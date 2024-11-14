import requests
import os
from pages.models import Assignments, StudentAssignments
import anthropic
from datetime import datetime
import json
CLAUDE_API_URL = "https://api.anthropic.com/v1/tasks"
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

def get_assignment_breakdown(assignment_id):
    """Fetch assignment details from the database and get a breakdown from Claude API."""
    # Fetch the assignment from the database
    print(assignment_id)
    assignment = Assignments.get_by_id(assignment_id)
    
    if not assignment:
        raise Exception(f"Assignment with ID {assignment_id} not found.")

    # # Fetch student assignments to prioritize
    # assignments = Assignments.get_by_course_id(assignment['course_id'])  # You may want to filter by student_id
    # prioritized_tasks = []

    # for assignment in assignments:
    #     if assignment.student == student_id and not assignment.completed:
    #         prioritized_tasks.append({
    #             "assignment_name": assignment['name'],
    #             "due_date": assignment['due_at'],
    #             "points_possible": assignment['points_possible'],
    #             "status": "Pending"
    #         })

    # Prepare the prompt for Claude API
    assignment_description = f"Assignment Name: {assignment['name']}\n" \
                             f"Description: {assignment['description']}\n" \
                             f"Due Date: {assignment['due_at']}\n" \
                             f"Points Possible: {assignment['points_possible']}\n" \
                             f"Prioritized Tasks:\n"

    # for task in prioritized_tasks:
    #     assignment_description += f"- {task['assignment_name']} (Due: {task['due_date']}, Points: {task['points_possible']}, Status: {task['status']})\n"

    print(assignment_description)
    client = anthropic.Anthropic(
        api_key=CLAUDE_API_KEY,
    )

    # Replace placeholders like {{CURRENT_DATE}} with real values,
    # because the SDK does not support variables.
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=8192,
        temperature=0,
        system="You are now an advanced academic planning assistant, specialized in helping students break down assignments and projects into manageable tasks and providing time estimates. Your goal is to help students organize their work effectively and plan their time efficiently.\n\n  When given an assignment or project description, please do the following:\n\n  1. Analyze the assignment or project carefully, considering its scope, complexity, and requirements.\n  2. Break down the assignment or project into a logical sequence of smaller, actionable tasks. Each task should be specific and clearly defined.\n  3. For each task, provide:\n     a) A brief description of what needs to be done\n     b) An estimated time range to complete the task (e.g., 1-2 hours, 2-3 days)\n     c) Any relevant tips or considerations for that specific task\n     d) Suggestions for relevant YouTube videos that could help the student complete the task (include video titles and links)\n  4. Organize the tasks in a logical order, considering any dependencies between tasks.\n  5. Provide a total estimated time range for the entire assignment or project.\n  6. Offer suggestions for how to distribute the work over time (e.g., daily goals, weekly targets) based on the given deadline, if any.\n  7. Include recommendations for breaks and buffer time to account for unexpected challenges or revisions.\n  8. If relevant, suggest any resources or tools that might be helpful for specific tasks.\n  9. Provide a brief explanation of your reasoning behind the task breakdown and time estimates.\n  10. Offer advice on how to track progress and adjust the plan if needed.\n\n  When providing time estimates, consider the following factors:\n  • The typical workload and pace of an average student\n  • The complexity of each task\n  • Any research or preparation required\n  • Time needed for review and revisions\n\n  Be prepared to adjust your estimates and recommendations based on additional information about the student's skill level, available time, or other relevant factors.\n\n Only return JSON. Your goal is to provide a practical, actionable plan that will help students manage their academic work effectively.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"You are an advanced academic planning assistant, specialized in helping students break down assignments and projects into manageable tasks with accurate time estimates. Your goal is to provide a comprehensive, well-organized plan that will help students manage their academic work effectively and stay motivated throughout the process.\nHere is the information about the current assignment:\n<assignment_description>\n{assignment['description']}\n</assignment_description>\n<assignment_title>\n{assignment['name']}\n</assignment_title>\n<current_date>\n{current_date}\n</current_date>\n<assignment_due_date>\n{assignment['due_at']}\n</assignment_due_date>\nYour task is to analyze this assignment and create a detailed breakdown of tasks, time estimates, helpful resources, and motivational elements. Follow these steps:\n1. Analyze the assignment description, considering its scope, complexity, and requirements.\n2. Break down the assignment into a logical sequence of smaller, actionable tasks.\n3. For each task, provide:\n    a) A brief description of what needs to be done\n    b) An estimated time range to complete the task (e.g., \"1-2 hours\", \"2-3 days\")\n    c) Relevant tips or considerations\n    d) Suggestions for helpful YouTube videos (include titles and links)\n    e) Priority level (High/Medium/Low)\n    f) Potential distractions and mitigation strategies\n    g) Focus techniques\n    h) A small reward or motivational element upon completion\n4. Calculate a total estimated time range for the entire assignment.\n5. Suggest how to distribute the work over time based on the given deadline.\n6. Include recommendations for breaks and buffer time.\n7. Suggest additional helpful resources or tools.\n8. Provide ADHD-specific strategies for time management, focus improvement, and motivation.\n9. Design a reward system to keep students motivated throughout the assignment.\n\nAnalyze the assignment and include this analysis in the JSON output. In this analysis:\n1. Quote key phrases from the assignment description that indicate specific tasks or requirements.\n2. List out each identified task, numbering them as you go.\n3. For each task, estimate a time range and explain your reasoning.\n4. Consider any dependencies between tasks and explain how this affects their order.\n5. Sum up the estimated time ranges to get a total time estimate for the entire assignment.\n6. Evaluate the overall complexity of the assignment on a scale of 1-10, considering factors such as research requirements, technical difficulty, and time constraints.\n7. Identify key skills required for the assignment.\n8. Brainstorm potential challenges and how to overcome them.\n9. Consider motivational elements and rewards that could be incorporated into the plan.\n\nGenerate a JSON object containing all the required information. The JSON structure should be as follows:\n\n```json\n{{\n\"analysis\": {{\n    \"thought_process\": {{\n        \"initial_assessment\": \"\",\n        \"complexity_evaluation\": \"\",\n        \"complexity_scores\": {{\n            \"overall_complexity\": 0,\n            \"research_complexity\": 0,\n            \"technical_complexity\": 0,\n            \"time_complexity\": 0,\n            \"complexity_explanation\": \"\"\n        }},\n        \"key_requirements\": [],\n        \"potential_challenges\": [],\n        \"skill_level_considerations\": \"\"\n    }}\n}},  \n\"assignment_breakdown\": [\n    {{\n        \"task_number\": 0,\n        \"description\": \"\",\n        \"estimated_time\": \"\",\n        \"due_date\": \"\",\n        \"tips\": \"\",\n        \"youtube_resources\": [\n            {{\n                \"title\": \"\",\n                \"link\": \"\"\n            \}}\n        ],\n        \"priority\": \"\",\n        \"potential_distractions\": [],\n        \"distraction_mitigation\": \"\",\n        \"focus_techniques\": [],\n        \"reward\": \"\"\n    }}\n],\n\"total_estimated_time\": \"\",\n\"work_distribution\": \"\",\n\"breaks_and_buffer\": \"\",\n\"additional_resources\": \[\],\n\"reasoning\": \"\",\n\"progress_tracking\": \"\",\n\"adhd_specific_strategies\": {{\n    \"time_management\": [],\n    \"focus_improvement\": [],\n    \"motivation_boosters\": []\n}},\n\"reward_system\": {{\n    \"milestone_rewards\": [],\n    \"completion_reward\": \"\",    \n    \"progress_visualization\": \"\"\n}}\n}}\n}}\n\nEnsure that your JSON output is properly formatted, with correct indentation and nesting of objects and arrays. Each key-value pair should be on a separate line, and arrays should have each item on a new line. Use double quotes for all strings and property names.\n\nRemember to include motivational elements and rewards throughout the task breakdown and in the dedicated reward_system section. These should be designed to give students \"dopamine hits\" to stay motivated and engaged in completing their homework."
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
    )

    # Log the raw response
    print("Raw API response:", message)

    if message.stop_reason == "end_turn":
        try:
            # Assuming message.content is a list of TextBlock objects
            response_text = message.content[0].text  # Get the text from the first block
            response_text = "{" + response_text[:response_text.rfind("}") + 1]
            print("Response text:", response_text)  # Log the response text
            breakdown = json.loads(response_text)  # Convert JSON string to dictionary
            print("Breakdown:", breakdown)
            return breakdown
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to decode JSON response: {e}")
    else:
        raise Exception(f"Failed to get assignment breakdown: {message.status_code} {message.text}")

def fetch_all_assignments():
    """Fetch all assignments from the database."""
    return Assignments.get_all()

def fetch_assignments_by_course(course_id):
    """Fetch assignments for a specific course from the database."""
    return Assignments.get_by_course_id(course_id)