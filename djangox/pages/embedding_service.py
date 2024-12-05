from tenacity import retry, wait_random_exponential, stop_after_attempt
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import numpy as np
import os
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from openai import OpenAI
from django.db import models

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        self.tfidf = TfidfVectorizer(max_features=1536)
        self.client = OpenAI()
        
        try:
            self.embeddings = OpenAIEmbeddings(api_key=os.getenv('OPENAI_API_KEY'))
            self.use_openai = True
        except Exception as e:
            logger.warning(f"Failed to initialize OpenAI embeddings: {e}")
            self.use_openai = False
    
    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
    def _get_embedding(self, text: str, model="text-embedding-3-small") -> list[float]:
        """Get embeddings with retry logic for better rate limit handling"""
        return self.client.embeddings.create(
            input=[text], 
            model=model
        ).data[0].embedding
    
    def create_embeddings(self, text, file_name):
        """Create embeddings for a text document"""
        try:
            print(f"\n🔄 Creating embeddings for {file_name}")
            
            # Split text into chunks
            chunks = self.text_splitter.split_text(text)
            print(f"  📄 Split into {len(chunks)} chunks")
            
            if self.use_openai:
                try:
                    return self._create_openai_embeddings(chunks, text)
                except Exception as e:
                    logger.warning(f"OpenAI embeddings failed, falling back to TF-IDF: {e}")
                    self.use_openai = False
            
            return self._create_tfidf_embeddings(chunks, text)
                
        except Exception as e:
            print(f"  ❌ Error creating embeddings: {str(e)}")
            logger.error(f"Error creating embeddings for {file_name}: {e}")
            return None
    
    def _create_openai_embeddings(self, chunks, text):
        """Create embeddings using OpenAI with improved rate limiting"""
        chunk_embeddings = []
        for i, chunk in enumerate(chunks):
            embedding = self._get_embedding(chunk)
            chunk_embeddings.append({
                'chunk': chunk,
                'embedding': embedding,
                'index': i
            })
        
        doc_embedding = self._get_embedding(text[:8000])
        return {
            'doc_embedding': doc_embedding,
            'chunk_embeddings': chunk_embeddings
        }
    
    def _create_tfidf_embeddings(self, chunks, text):
        all_texts = chunks + [text[:8000]]
        tfidf_matrix = self.tfidf.fit_transform(all_texts)
        
        dense_embeddings = tfidf_matrix.toarray()
        
        norms = np.linalg.norm(dense_embeddings, axis=1, keepdims=True)
        normalized_embeddings = dense_embeddings / norms
        
        chunk_embeddings = []
        for i, chunk in enumerate(chunks):
            chunk_embeddings.append({
                'chunk': chunk,
                'embedding': normalized_embeddings[i].tolist(),
                'index': i
            })
        
        return {
            'doc_embedding': normalized_embeddings[-1].tolist(),
            'chunk_embeddings': chunk_embeddings
        }
    
    def find_similar_chunks(self, query, chunk_embeddings, top_k=3):
        try:
            print(f"\n🔍 Creating embedding for query: {query[:100]}...")
            query_embedding = self.embeddings.embed_query(query)
            print(f"  📊 Query embedding shape: {len(query_embedding)}")
            print(f"  📊 First 5 values: {query_embedding[:5]}")
            print(f"  📊 Last 5 values: {query_embedding[-5:]}")
            
            # Calculate similarities
            similarities = []
            print("\n  🔄 Calculating similarities with chunks:")
            for i, chunk_data in enumerate(chunk_embeddings):
                similarity = np.dot(query_embedding, chunk_data['embedding'])
                print(f"    Chunk {i+1}: {similarity:.4f}")
                similarities.append((similarity, chunk_data['chunk'], chunk_data['index']))
            
            # Sort by similarity
            similarities.sort(reverse=True)
            top_results = similarities[:top_k]
            print("\n  ✨ Top matches:")
            for i, (similarity, chunk, index) in enumerate(top_results, 1):
                print(f"    {i}. Similarity: {similarity:.4f}")
                print(f"       Chunk {index}: {chunk[:100]}...")
            
            return top_results
            
        except Exception as e:
            logger.error(f"Error finding similar chunks: {e}")
            return [] 