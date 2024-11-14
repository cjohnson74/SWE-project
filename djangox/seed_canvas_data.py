import json
import os
import django
from pathlib import Path
import requests
from django.utils import timezone
from dotenv import load_dotenv

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

# Set up Django
django.setup()

from pages.models import Assignments, Courses

# Load environment variables from the .env file
load_dotenv(dotenv_path=Path('.') / '.env')

# Configuration
CANVAS_API_URL = 'https://canvas.instructure.com/api/v1'
ACCESS_TOKEN = os.getenv('CANVAS_ACCESS_TOKEN')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
ENROLLMENT_TERM_ID = os.getenv('ENROLLMENT_TERM_ID')

# def drop_collections():
#     """Drop specified MongoDB collections"""
#     collections_to_drop = ['Courses', 'Assignments']
#     for collection_name in collections_to_drop:
#         db[collection_name].drop()
#         print(f"Dropped collection: {collection_name}")

def fetch_data_from_canvas(url, headers):
    """Fetch data from Canvas API"""
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_courses():
    """Fetch all courses from Canvas"""
    url = f"{CANVAS_API_URL}/courses"
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    return fetch_data_from_canvas(url, headers)

def fetch_assignments(course_id):
    """Fetch all assignments for a given course from Canvas"""
    url = f"{CANVAS_API_URL}/courses/{course_id}/assignments"
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    return fetch_data_from_canvas(url, headers)

def seed_data():
    """Seed courses and assignments into MongoDB"""
    courses = fetch_courses()

    # Insert each course into the MongoDB collection
    for course in courses:
        if course.get('enrollment_term_id', '') != int(ENROLLMENT_TERM_ID):
            continue
        print(f"Seeding course: {type(course)}")
        print(json.dumps(course, indent=4))
        course_instance, created = Courses.objects.update_or_create(
            course_id=course['id'],
            defaults={
                'name': course.get('name', ''),
                'course_code': course.get('course_code', ''),
                'created_at': course.get('created_at', ''),
                'workflow_state': course.get('workflow_state', ''),
            }
        )
        
        # Seed assignments for each course
        assignments = fetch_assignments(course_instance.course_id)
        for assignment in assignments:
            print(f"Seeding assignment: {assignment['name']}")
            print(json.dumps(assignment, indent=4))
            Assignments.objects.update_or_create(
                assignment_id=assignment['id'],
                defaults={
                    'canvas_id': assignment['id'],
                    'course': course_instance,
                    'name': assignment['name'],
                    'description': assignment.get('description', ''),
                    'due_at': assignment.get('due_at', ''),
                    'points_possible': assignment.get('points_possible', ''),
                    'submission_types': assignment['submission_types'][0] if 'submission_types' in assignment and assignment['submission_types'] else '',
                    'updated_at': assignment.get('updated_at', '')
                }
            )

    print(f"Seeded data into Django database")

if __name__ == '__main__':
    seed_data()
