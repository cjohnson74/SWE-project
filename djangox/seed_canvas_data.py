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

from pages.models import Assignments, Courses, Modules, ModuleItems

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

def fetch_data_from_canvas(url, headers, params=None):
    """Fetch data from Canvas API with optional parameters"""
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data from Canvas: {e}")
        raise

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

def fetch_modules(course_id):
    """Fetch all modules and their items from Canvas"""
    url = f"{CANVAS_API_URL}/courses/{course_id}/modules"
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    params = {
        'include[]': ['items', 'content_details']
    }
    try:
        modules = fetch_data_from_canvas(url, headers, params)
        print(f"✅ Successfully fetched {len(modules)} modules")
        return modules
    except Exception as e:
        print(f"❌ Error fetching modules: {e}")
        return []

def fetch_assignment_from_module_item(course_id, assignment_id):
    """Fetch assignment details using the assignment ID from a module item"""
    url = f"{CANVAS_API_URL}/courses/{course_id}/assignments/{assignment_id}"
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    try:
        return fetch_data_from_canvas(url, headers)
    except Exception as e:
        return None

def seed_data():
    courses = fetch_courses()

    for course in courses:
        if course.get('enrollment_term_id', '') != int(ENROLLMENT_TERM_ID):
            continue
        
        course_instance, created = Courses.objects.update_or_create(
            course_id=course['id'],
            defaults={
                'name': course.get('name', ''),
                'course_code': course.get('course_code', ''),
                'created_at': course.get('created_at', ''),
                'workflow_state': course.get('workflow_state', ''),
            }
        )
        
        # Track processed assignment IDs to avoid duplicates
        processed_assignments = set()
        
        # Fetch direct assignments
        direct_assignments = fetch_assignments(course_instance.course_id)
        for assignment in direct_assignments:
            processed_assignments.add(assignment['id'])
            Assignments.objects.update_or_create(
                assignment_id=assignment['id'],
                defaults={
                    'canvas_id': assignment['id'],
                    'course': course_instance,
                    'name': assignment.get('name', ''),
                    'description': assignment.get('description', ''),
                    'due_at': assignment.get('due_at', ''),
                    'points_possible': assignment.get('points_possible', ''),
                    'submission_types': assignment['submission_types'][0] if 'submission_types' in assignment and assignment['submission_types'] else '',
                    'updated_at': assignment.get('updated_at', '')
                }
            )
        
        # Process modules and their items
        modules = fetch_modules(course_instance.course_id)
        for module in modules:
            module_instance = Modules.objects.update_or_create(
                module_id=module['id'],
                defaults={
                    'course': course_instance,
                    'name': module.get('name', ''),
                    'position': module.get('position', 0),
                    'workflow_state': module.get('workflow_state', 'active'),
                    'unlock_at': module.get('unlock_at'),
                    'require_sequential_progress': module.get('require_sequential_progress', False),
                    'publish_final_grade': module.get('publish_final_grade', False),
                    'prerequisite_module_ids': module.get('prerequisite_module_ids', []),
                    'items_count': module.get('items_count', 0),
                    'state': module.get('state'),
                    'completed_at': module.get('completed_at'),
                    'published': module.get('published', True),
                }
            )[0]
            
            if 'items' in module and module['items']:
                for item in module['items']:
                    print(f"  📄 Processing item: {item.get('title')}")
                    content_details = item.get('content_details', {})
                    # Process assignments found in modules
                    if item.get('type') in ['Assignment', 'Quiz'] and item.get('content_id'):
                        if item['content_id'] not in processed_assignments:
                            assignment = fetch_assignment_from_module_item(
                                course_instance.course_id, 
                                item['content_id']
                            )
                            if assignment:
                                processed_assignments.add(assignment['id'])
                                Assignments.objects.update_or_create(
                                    assignment_id=assignment['id'],
                                    defaults={
                                        'canvas_id': assignment['id'],
                                        'course': course_instance,
                                        'name': assignment.get('name', ''),
                                        'description': assignment.get('description', ''),
                                        'due_at': assignment.get('due_at', ''),
                                        'points_possible': assignment.get('points_possible', ''),
                                        'submission_types': assignment['submission_types'][0] if 'submission_types' in assignment and assignment['submission_types'] else '',
                                        'updated_at': assignment.get('updated_at', '')
                                    }
                                )
                    
                    # Create module item
                    ModuleItems.objects.update_or_create(
                        item_id=item['id'],
                        defaults={
                            'module': module_instance,
                            'title': item.get('title', ''),
                            'position': item.get('position', 0),
                            'indent': item.get('indent', 0),
                            'type': item.get('type', ''),
                            'content_id': item.get('content_id'),
                            'html_url': item.get('html_url', ''),
                            'url': item.get('url', ''),
                            'page_url': item.get('page_url', ''),
                            'external_url': item.get('external_url', ''),
                            'new_tab': item.get('new_tab', False),
                            'completion_requirement': item.get('completion_requirement', {}),
                            'content_details': content_details,
                            'published': item.get('published', True),
                        }
                    )

if __name__ == '__main__':
    seed_data()
