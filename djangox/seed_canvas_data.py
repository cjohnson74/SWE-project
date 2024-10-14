import json
import os
from pathlib import Path
import requests
from pages.models import Assignments, Courses
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv(dotenv_path=Path('.') / '.env')

# Configuration
CANVAS_API_URL = 'https://canvas.instructure.com/api/v1'
ACCESS_TOKEN = os.getenv('CANVAS_ACCESS_TOKEN')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
ENROLLMENT_TERM_ID = os.getenv('ENROLLMENT_TERM_ID')

# MongoDB client setup
client = MongoClient(DB_HOST)
db = client[DB_NAME]

def drop_collections():
    """Drop specified MongoDB collections"""
    collections_to_drop = ['Courses', 'Assignments']
    for collection_name in collections_to_drop:
        db[collection_name].drop()
        print(f"Dropped collection: {collection_name}")

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

def fetch_quizzes(course_id):
    """Fetch all quizzes for a given course from Canvas"""
    url = f"{CANVAS_API_URL}/courses/{course_id}/quizzes"
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    return fetch_data_from_canvas(url, headers)

def fetch_files(course_id):
    """Fetch all files for a given course from Canvas"""
    url = f"{CANVAS_API_URL}/courses/{course_id}/files"
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def seed_data():
    """Seed courses and assignments into MongoDB"""
    # Drop collections if they exist
    print("Dropping collections")
    drop_collections()

    # Fetch courses from Canvas
    print("Fetching courses")
    courses = fetch_courses()

    # Insert each course into the MongoDB collection
    for course in courses:
        if course.get('enrollment_term_id', '') != int(ENROLLMENT_TERM_ID):
            continue
        print(f"Seeding course: {type(course)}")
        print(json.dumps(course, indent=4))
        course_data = {
            'course_id': course['id'],    
            'calendar_url': course.get('calendar', {}).get('calendar_url', ''),
            'name': course.get('name', ''),
            'course_code': course.get('course_code', ''),
            'created_at': course.get('created_at', ''),
            'workflow_state': course.get('workflow_state', ''),
        }
        
        # Insert or update the course in the database
        db['Courses'].update_one(
            {'course_id': course_data.get('course_id', '')},
            {'$set': course_data},
            upsert=True
        )
        
        # Seed assignments for each course
        assignments = fetch_assignments(course_data['course_id'])
        for assignment in assignments:
            print(f"Seeding assignment: {assignment['name']}")
            assignment_data = {
                'assignment_id': assignment['id'],
                'course_id': course_data['course_id'],
                'name': assignment['name'],
                'description': assignment.get('description', ''),
                'due_at': assignment.get('due_at', ''),
                'points_possible': assignment.get('points_possible', ''),
                'submission_types': assignment['submission_types'][0] if 'submission_types' in assignment and assignment['submission_types'] else '',
                'updated_at': assignment.get('updated_at', '')
            }
            db['Assignments'].update_one(
                {'assignment_id': assignment_data['assignment_id']},
                {'$set': assignment_data},
                upsert=True
            )
        
        # # Fetch and seed files for each course
        # files = fetch_files(course_data['course_id'])
        # for file in files:
        #     print(f"Seeding file: {file['name']}")
        #     file_data = {
        #         'file_id': file['id'],
        #         'folder_id': file['folder_id'],
        #         'course_id': course_data['course_id'],
        #         'filename': file['filename'],
        #         'display_name': file['display_name'],
        #         'url': file['url'],
        #         'size': file['size'],
        #         'content_type': file['content_type'],
        #         'created_at': file['created_at'],
        #         'modified_at': file['modified_at'],
        #     }
        #     db['Files'].update_one(
        #         {'file_id': file_data['file_id']},
        #         {'$set': file_data},
        #         upsert=True
        #     )

    print(f"Seeded data into MongoDB {DB_NAME}")

if __name__ == '__main__':
    seed_data()
