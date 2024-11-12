import requests
import os

CLAUDE_API_URL = "https://api.anthropic.com/v1/tasks"
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

def get_assignment_breakdown(assignment_description):
    headers = {
        "Authorization": f"Bearer {CLAUDE_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "claude-3-5-sonnet-20240620",
        "prompt": assignment_description,
    }

    response = requests.post(CLAUDE_API_URL, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get assignment breakdown: {response.status_code} {response.text}")
    