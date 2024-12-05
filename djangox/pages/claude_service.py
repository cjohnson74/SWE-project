import requests
import os
from pages.models import AssignmentFile, Assignments
import anthropic
from datetime import datetime
import json
import logging
import base64
from pdf2image import convert_from_path
from io import BytesIO
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
import numpy as np

# Set up logger
logger = logging.getLogger(__name__)
CLAUDE_API_URL = "https://api.anthropic.com/v1/tasks"
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

def get_assignment_breakdown(assignment_id):
    """Fetch assignment details from the database and get a breakdown from Claude API."""
    logger.debug(f"Getting breakdown for assignment: {assignment_id}")
    assignment = Assignments.objects.get(assignment_id=assignment_id)
    
    if not assignment:
        raise Exception(f"Assignment with ID {assignment_id} not found.")

    # Get file contents
    file_contents = get_assignment_files_content(assignment)
    
    # Format file contents for Claude
    formatted_files = []
    for file_content in file_contents:
        try:
            # Parse the JSON string if it isn't already a dict
            if isinstance(file_content, str):
                content_dict = json.loads(file_content)
            else:
                content_dict = file_content
                
            formatted_files.append({
                "file_name": content_dict.get("file_name", "Unknown"),
                "content": content_dict.get("file_content", "")
            })
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse file content as JSON: {e}")
            logger.error(f"Raw content: {file_content}")
            continue

    # Prepare the message for Claude
    files_text = "\n\n".join([
        f"File: {f['file_name']}\nContent: {f['content']}"
        for f in formatted_files
    ])

    print(assignment.name, assignment.description)
    print(files_text)

    messages = [{
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": f"""Given this assignment and its files:

                Assignment Name: {assignment.name}
                Description: {assignment.description}

                Files:
                {files_text}

                Your goal is to analyze this assignment and create a detailed breakdown of ALL the smaller, actionable tasks that the student needs to complete to finish the assignment on time, including time estimates, helpful resources, and motivational elements. Follow these steps:
                1. Analyze the assignment description, considering its scope, complexity, and requirements.
                2. Break down the assignment into a logical sequence of smaller, actionable tasks.
                3. For each task, provide:
                    a) A title for the task
                    b) A detailed description of what needs to be done
                    c) A due date for the task
                    d) An estimated time range to complete the task (e.g. 5-10 minutes, 1-2 hours, 2-3 days)
                    e) Relevant tips or considerations
                    f) Suggestions for helpful YouTube videos (include titles and links)
                    g) Priority level (High/Medium/Low)
                    h) Potential distractions and mitigation strategies
                    i) Focus techniques
                    j) A small reward or motivational element upon completion
                4. Calculate a total estimated time range for the entire assignment.
                5. Suggest how to distribute the work over time based on the given deadline.
                6. Include recommendations for breaks and buffer time.
                7. Suggest additional helpful resources or tools.
                8. Provide ADHD-specific strategies for time management, focus improvement, and motivation.
                9. Design a reward system to keep students motivated throughout the assignment.

                Analyze the assignment and include this analysis in the JSON output. In this analysis:
                1. Quote key phrases from the assignment description that indicate specific tasks or requirements.
                2. List out each identified task, numbering them as you go.
                3. For each task, estimate a time range and explain your reasoning.
                4. Consider any dependencies between tasks and explain how this affects their order.
                5. Sum up the estimated time ranges to get a total time estimate for the entire assignment.
                6. Evaluate the overall complexity of the assignment on a scale of 1-10, considering factors such as research requirements, technical difficulty, and time constraints.
                7. Identify key skills required for the assignment.
                8. Brainstorm potential challenges and how to overcome them.
                9. Consider motivational elements and rewards that could be incorporated into the plan.

                Generate a JSON object containing all the required information. 
                The JSON structure should be as follows and make sure I can parse it into a python dictionary:
                {{
                    "analysis": {{
                        "thought_process": {{
                            "initial_assessment": "string",
                            "complexity_evaluation": "string",
                            "complexity_scores": {{
                                "overall_complexity": "1-10",
                                "research_complexity": "1-10",
                                "technical_complexity": "1-10",
                                "time_complexity": "1-10",
                                "complexity_explanation": "string"
                            }},
                            "key_requirements": ["string"],
                            "potential_challenges": ["string"],
                            "skill_level_considerations": "string"
                        }}
                    }},
                    "total_estimated_time": "string",
                    "work_distribution": "string",
                    "breaks_and_buffer": "string",
                    "assignment_breakdown": [
                        {{
                            "task_number": "integer",
                            "title": "string",
                            "description": "string",
                            "estimated_time": "string",
                            "due_date": "ISO date string",
                            "tips": "string",
                            "priority": "high|medium|low",
                            "potential_distractions": ["string"],
                            "distraction_mitigation": "string",
                            "focus_techniques": ["string"],
                            "reward": "string",
                            "youtube_resources": [
                                {{
                                    "title": "string",
                                    "link": "string"
                                }}
                            ]
                        }}
                    ]
                }},
                "adhd_specific_strategies": {{
                    "time_management": ["string"],
                    "focus_improvement": ["string"],
                    "motivation_boosters": ["string"]
                }},
                "reward_system": {{
                    "milestone_rewards": ["string"],
                    "completion_reward": "string",
                    "progress_visualization": "string"
                }}
                Ensure that your JSON output is properly formatted, with correct indentation and nesting of objects and arrays. Each key-value pair should be on a separate line, and arrays should have each item on a new line. Use double quotes for all strings and property names.

                Remember to include motivational elements and rewards throughout the task breakdown and in the dedicated reward_system section. These should be designed to give students \"dopamine hits\" to stay motivated and engaged in completing their homework."""
            }
        ]
    }]

    try:
        response_text = call_claude_api(messages)
        breakdown_data = parse_claude_response(response_text)
        return breakdown_data
    except Exception as e:
        logger.error(f"Error getting breakdown from Claude: {str(e)}")
        raise

def fetch_all_assignments():
    """Fetch all assignments from the database."""
    return Assignments.objects.all()

def fetch_assignments_by_course(course_id):
    """Fetch assignments for a specific course from the database."""
    return Assignments.objects.filter(course_id=course_id)

def get_assignment_files_content(assignment):
    """Get the content of the specified files."""
    files = AssignmentFile.objects.filter(assignment=assignment)
    print(f"\n=== Starting processing for {len(files)} files ===")
    files_content = []
    
    for file in files:
        print(f"\n--- Processing file: {file.file_name} ---")
        logger.debug(f"Processing file: {file.file_name}")
        
        # Check if we already have Claude's response
        if file.claude_response:
            try:
                print(f"✅ Using existing Claude response for {file.file_name} (cached) {file.claude_response}")
                content_dict = json.loads(file.claude_response)
                files_content.append(content_dict)
                continue
            except json.JSONDecodeError as e:
                print(f"❌ Cached response is invalid, reprocessing file. {e}")
        
        try:
            file_type = file.file_type.lower()
            is_image = file_type in ['jpg', 'jpeg', 'png', 'gif', 'bmp']
            is_pdf = file_type == 'pdf'
            
            if is_pdf:
                try:
                    # Save raw PDF content
                    with file.file.open('rb') as pdf_file:
                        file.content = base64.b64encode(pdf_file.read()).decode('utf-8')
                    
                    images = convert_from_path(file.file.path, dpi=300, fmt='PNG', grayscale=False)
                    print(f"✅ Successfully converted PDF to {len(images)} images")
                    
                    image_contents = []
                    for i, image in enumerate(images):
                        print(f"Processing PDF page {i+1}/{len(images)}")
                        img_byte_arr = BytesIO()
                        image.save(img_byte_arr, format='PNG', optimize=False, quality=100)
                        img_byte_arr = img_byte_arr.getvalue()
                        image_data = base64.b64encode(img_byte_arr).decode('utf-8')
                        
                        messages = [{
                            "role": "user",
                            "content": [
                                {
                                    "type": "image",
                                    "source": {
                                        "type": "base64",
                                        "media_type": "image/png",
                                        "data": image_data,
                                    }
                                },
                                {
                                    "type": "text",
                                    "text": f"This is page {i+1} of a PDF uploaded by a student for a course assignment. It may contain handwritten text, code, diagrams, and other content. Please carefully extract and transcribe all handwritten text, code, diagram descriptions, and other content, maintaining the original structure and layout. Return the content in a valid JSON object with this structure: {{\"file_name\": \"{file.file_name}\", \"file_content\": \"content\"}}"
                                }
                            ]
                        },
                        {
                            "role": "assistant",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "{"
                                }
                            ]
                        }
                        ]
                        print(f"Calling Claude API for page {i+1}...")
                        response_text = call_claude_api(messages)
                        content_dict = parse_claude_response(response_text, file.file_name)
                        image_contents.append(content_dict)
                        print(f"✅ Successfully processed page {i+1}")

                    # Save combined PDF content
                    if image_contents:
                        combined_content = {
                            "file_name": file.file_name,
                            "file_content": "\n\n".join(page["file_content"] for page in image_contents)
                        }
                        print(f"🔍 Combined Claude's response: {combined_content}")
                        file.claude_response = json.dumps(combined_content)
                        file.save()
                        files_content.extend(image_contents)

                except Exception as e:
                    print(f"❌ Failed to process PDF: {e}")
                    logger.error(f"Failed to process PDF {file.file_name}: {e}")
                    continue

            elif is_image:
                try:
                    # Save raw image content
                    with file.file.open('rb') as img_file:
                        image_data = base64.b64encode(img_file.read()).decode('utf-8')
                        file.content = image_data
                    
                    image_media_type = f"image/{file_type}"
                    if file_type == 'jpg':
                        image_media_type = "image/jpeg"
                        
                    messages = [{
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": image_media_type,
                                    "data": image_data,
                                }
                            },
                            {
                                "type": "text",
                                "text": f"Extract the content from this image uploaded by a student for a course assignment. It may contain handwritten text, code, diagrams, and other content. Please carefully extract and transcribe all handwritten text, code, diagram descriptions, and other content, maintaining the original structure and layout. Return the content in a valid JSON object with this structure: {{\"file_name\": \"{file.file_name}\", \"file_content\": \"content\"}}"
                            }
                        ]
                    },
                    {
                        "role": "assistant",
                        "content": [
                            {
                                "type": "text",
                                "text": "{"
                            }
                        ]
                    }
                    ]
                    print("Calling Claude API for image interpretation...")
                    response_text = call_claude_api(messages)
                    content_dict = parse_claude_response(response_text, file.file_name)
                    
                    # Save Claude's response
                    file.claude_response = json.dumps(content_dict)
                    file.save()
                    
                    files_content.append(content_dict)
                    print("✅ Successfully processed image")
                    
                except Exception as e:
                    print(f"❌ Failed to process image: {e}")
                    logger.error(f"Failed to process image {file.file_name}: {e}")
                    continue

            else:  # Text-based files
                try:
                    # Save raw text content
                    with file.file.open('r') as text_file:
                        file_content = text_file.read()
                        file.content = file_content
                    
                    content_dict = {
                        "file_name": file.file_name,
                        "file_content": file_content
                    }
                    
                    # Save content directly for text files
                    file.claude_response = json.dumps(content_dict)
                    file.save()
                    
                    files_content.append(content_dict)
                    print("✅ Successfully processed text file")
                    
                except Exception as e:
                    print(f"❌ Failed to process text file: {e}")
                    logger.error(f"Failed to process text file {file.file_name}: {e}")
                    continue

            print(f"💬 Claude's response for {file.file_name}: {file.claude_response}")

        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            logger.error(f"Unexpected error processing file {file.file_name}: {e}")
            continue
            
    if not files_content:
        print("⚠️ Warning: No files were successfully processed")
        logger.warning(f"No files were successfully processed for assignment {assignment.name}")
    else:
        print(f"\n✅ Successfully processed {len(files_content)} files")
        
    return files_content

def parse_claude_response(response_text, file_name=None):
    """Helper function to parse Claude's response and extract JSON."""
    print("Parsing Claude response...")
    if not response_text:
        print("❌ Empty response from Claude")
        raise ValueError("Empty response from Claude")
    
    if not response_text.startswith('{'):
        response_text = "{" + response_text
        
    # Clean and normalize the response text
    try:
        # Remove newlines and spaces between JSON elements
        cleaned_text = ' '.join(response_text.split())
        # Handle special mathematical symbols
        cleaned_text = cleaned_text.encode('ascii', 'ignore').decode('ascii')
        
        print("Attempting to parse cleaned JSON...")
        result = json.loads(cleaned_text)
        print("✅ Successfully parsed response")
        
        # Print the extracted file contents
        if 'file_content' in result:
            print(f"\n📄 File Contents Extracted from Claude for {file_name}:")
            print(result['file_content'])
        
        return result
    except json.JSONDecodeError as e:
        print("⚠️ Initial JSON parsing failed, attempting alternative method...")
        try:
            # Try to extract JSON object and clean it
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            
            if start == -1 or end == -1:
                print("❌ No JSON object found in response")
                raise ValueError("No JSON object found in response")
                
            json_str = response_text[start:end]
            # Clean the extracted JSON string
            json_str = json_str.replace('\n', '\\n').replace('\r', '\\r')
            json_str = json_str.encode('ascii', 'ignore').decode('ascii')
            
            result = json.loads(json_str)
            print("✅ Successfully extracted and parsed JSON")
            
            # Print the extracted file contents
            if 'file_content' in result:
                print(f"\n📄 File Contents Extracted from Claude for {file_name}:")
                print(result['file_content'])
            
            return result
            
        except (json.JSONDecodeError, ValueError) as e:
            print(f"❌ Failed to parse response: {e}")
            logger.error(f"Failed to parse response for {file_name}: {e}")
            logger.error(f"Response text: {response_text}")
            raise

def call_claude_api(messages):
    """Helper function to call Claude API."""
    print("Calling Claude API...")
    try:
        client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=8192,
            temperature=0,
            messages=messages
        )
        print("✅ Claude API call successful")
        return response.content[0].text.strip()
    except anthropic.APIError as e:
        print(f"❌ Claude API error: {e}")
        logger.error(f"Claude API error: {e}")
        raise
    except Exception as e:
        print(f"❌ Unexpected Claude API error: {e}")
        logger.error(f"Unexpected error calling Claude API: {e}")
        raise

