from celery import shared_task
from .models import AssignmentFile
from .embedding_service import EmbeddingService
from datetime import datetime

@shared_task
def generate_embeddings(file_id):
    print(f"\n🔄 Starting embedding generation for file ID: {file_id}")
    try:
        file = AssignmentFile.objects.get(id=file_id)
        print(f"✓ Found file: {file.file_name}")
        
        # Verify file content exists
        if not file.content and not file.claude_response:
            print("❌ No content available for embedding generation")
            return False
            
        embedding_service = EmbeddingService()
        
        # Generate embeddings
        print("📊 Generating embeddings...")
        print(f"  - Content length: {len(file.content or file.claude_response)} characters")
        
        embeddings_data = embedding_service.create_embeddings(
            file.content or file.claude_response,
            file.file_name
        )
        
        if embeddings_data:
            print("✓ Embeddings generated successfully")
            print(f"  - Document embedding size: {len(embeddings_data['doc_embedding'])}")
            print(f"  - Number of chunks: {len(embeddings_data['chunk_embeddings'])}")
            
            file.set_embedding(embeddings_data['doc_embedding'])
            file.chunk_embeddings = embeddings_data['chunk_embeddings']
            file.last_embedded = datetime.now()
            file.save()
            print("✓ Saved embeddings to database")
            return True
            
        print("⚠️ No embeddings data generated")
        return False
        
    except Exception as e:
        print(f"❌ Error generating embeddings: {e}")
        return False