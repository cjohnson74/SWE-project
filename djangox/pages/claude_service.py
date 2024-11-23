import requests
import os
from pages.models import AssignmentFile, Assignments
import anthropic
from datetime import datetime
import json
import logging
import base64

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

                Your task is to analyze this assignment and create a detailed breakdown of tasks, time estimates, helpful resources, and motivational elements. Follow these steps:
                1. Analyze the assignment description, considering its scope, complexity, and requirements.
                2. Break down the assignment into a logical sequence of smaller, actionable tasks.
                3. For each task, provide:
                    a) A brief description of what needs to be done
                    b) An estimated time range to complete the task (e.g., "1-2 hours", "2-3 days")
                    c) Relevant tips or considerations
                    d) Suggestions for helpful YouTube videos (include titles and links)
                    e) Priority level (High/Medium/Low)
                    f) Potential distractions and mitigation strategies
                    g) Focus techniques
                    h) A small reward or motivational element upon completion
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
        client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=8192,
            temperature=0,
            messages=messages
        )

        # Get the response text
        response_text = response.content[0].text.strip()
        logger.debug(f"Raw response text: {response_text[:200]}...")  # Log first 200 chars

        try:
            # First attempt: Try to parse the entire response
            breakdown_data = json.loads(response_text)
            return breakdown_data
        except json.JSONDecodeError:
            # Second attempt: Try to extract JSON object
            start = response_text.find('{')
            end = response_text.rfind('}') + 1

            if start != -1 and end != -1:
                json_str = response_text[start:end]
                logger.debug(f"Extracted JSON string: {json_str[:200]}...")
                
                # Add missing braces if necessary
                if not json_str.startswith('{'):
                    json_str = '{' + json_str
                if not json_str.endswith('}'):
                    json_str = json_str + '}'
                
                try:
                    breakdown_data = json.loads(json_str)
                    return breakdown_data
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse extracted JSON: {e}")
                    logger.error(f"Extracted JSON string: {json_str}")
                    raise ValueError(f"Invalid JSON format: {e}")
            else:
                logger.error("No JSON object found in response")
                logger.error(f"Response text: {response_text}")
                raise ValueError("Could not find JSON object in response")

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
    """Get the content of the assignment files."""
    logger.debug(f"Processing files for assignment: {assignment.name}")
    assignment_files_content = []
    
    for file in AssignmentFile.objects.filter(assignment=assignment):
        logger.debug(f"Processing file: {file.file_name}")
        
        # Determine if file is an image based on file type
        is_image = file.file_type.lower() in ['jpg', 'jpeg', 'png', 'gif', 'bmp']
        
        if is_image:
            try:
                # Read image file and encode as base64
                with file.file.open('rb') as img_file:
                    image_data = base64.b64encode(img_file.read()).decode('utf-8')
                
                # Determine media type based on file extension
                image_media_type = f"image/{file.file_type.lower()}"
                if file.file_type.lower() == 'jpg':
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
                            "text": "Extract the content from this image and return it in a valid JSON object with this structure: {\"file_name\": \"filename\", \"file_content\": \"content\"}"
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
            except Exception as e:
                logger.error(f"Error processing image file {file.file_name}: {str(e)}")
                continue
        else:
            # Handle text-based files
            messages = [{
                "role": "user",
                "content": [{
                    "type": "text",
                    "text": f"Return a valid JSON object in this format: {{\"file_name\": \"{file.file_name}\", \"file_content\": \"{file.content}\"}}"
                }]
                },
                {
                    "role": "assistant",
                    "content": [{
                        "type": "text",
                        "text": "{"
                    }]
                }
            ]
        
        try:
            client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=8192,
                temperature=0,
                messages=messages
            )

            response_text = response.content[0].text.strip()

            # Add missing braces if necessary
            if not response_text.startswith('{'):
                response_text = '{' + response_text
            if not response_text.endswith('}'):
                response_text = response_text + '}'

            try:
                # Try to parse the entire response as JSON first
                content_dict = json.loads(response_text)
            except json.JSONDecodeError:
                # If that fails, try to extract JSON from the response
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                
                if start != -1 and end != -1:
                    json_str = response_text[start:end]
                    try:
                        content_dict = json.loads(json_str)
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse extracted JSON for file {file.file_name}: {e}")
                        logger.error(f"Extracted JSON string: {json_str}")
                        continue
                else:
                    logger.error(f"No JSON object found in response for file {file.file_name}")
                    logger.error(f"Response text: {response_text}")
                    continue
            
            assignment_files_content.append(content_dict)
            logger.debug(f"Successfully processed file: {file.file_name}")

        except Exception as e:
            logger.error(f"Error processing file {file.file_name}: {str(e)}")
            continue
            
    return assignment_files_content