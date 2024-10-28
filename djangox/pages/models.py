from pymongo import MongoClient
from django.conf import settings
from datetime import datetime

class MongoDBClient:
    def __init__(self):
        self.client = MongoClient(settings.MONGODB_SETTINGS['host'])
        self.db = self.client[settings.MONGODB_SETTINGS['database']]

# Create your models here.
class Document:
    collection_name = "Documents"

    def __init__(self, title=None, file_path=None):
        self.title = title
        self.file_path = file_path
        self.uploaded_at = datetime.now()

    def save(self):
        document = {
            "title": self.title,
            "file_path": self.file_path,
            "uploaded_at": self.uploaded_at,
        }
        client = MongoDBClient()
        client.db[self.collection_name].insert_one(self.__dict__)

    @staticmethod
    def get_all():
        return list(settings.MONGO_DB.documents.find())
                    
class Students():
    collection_name = 'Students'

    def __init__(self, canvas_id, name, sortable_name, short_name, login_id, email, avatar_url):
        self.canvas_id = canvas_id
        self.name = name
        self.sortable_name = sortable_name
        self.short_name = short_name
        self.login_id = login_id
        self.email = email
        self.avatar_url = avatar_url
    
    def save(self):
        client = MongoDBClient()
        students_collection = client.db[self.collection_name]
        students_collection.insert_one(self.__dict__)

    @staticmethod
    def get_all():
        client = MongoDBClient()
        students_collection = client.db[Students.collection_name]
        return list(students_collection.find())
    
    @staticmethod
    def get_by_id(canvas_id):
        client = MongoDBClient()
        students_collection = client.db[Students.collection_name]
        return students_collection.find_one({'canvas_id': canvas_id})
    
    @staticmethod
    def delete(canvas_id):
        client = MongoDBClient()
        students_collection = client.db[Students.collection_name]
        students_collection.delete_one({'canvas_id': canvas_id})

    @staticmethod
    def update(canvas_id, updates):
        client = MongoDBClient()
        students_collection = client.db[Students.collection_name]
        students_collection.update_one({'canvas_id': canvas_id}, {'$set': updates})

class Courses():
    collection_name = 'Courses'

    def __init__(self, course_id, account_id, apply_assignment_group_weights, blueprint, calendar, course_code, course_color, created_at, default_view, end_at, enrollment_term_id, enrollments, friendly_name, grade_passback_setting, grading_standard_id, hide_final_grades, homeroom_course, id, is_public, is_public_to_auth_users, license, name, public_syllabus, public_syllabus_to_auth, restrict_enrollments_to_course_dates, root_account_id, start_at, storage_quota_mb, template, time_zone, uuid, workflow_state):
        self.course_id = course_id
        self.account_id = account_id
        self.apply_assignment_group_weights = apply_assignment_group_weights
        self.blueprint = blueprint
        self.calendar = calendar
        self.course_code = course_code
        self.course_color = course_color
        self.created_at = created_at
        self.default_view = default_view
        self.end_at = end_at
        self.enrollment_term_id = enrollment_term_id
        self.enrollments = enrollments
        self.friendly_name = friendly_name
        self.grade_passback_setting = grade_passback_setting
        self.grading_standard_id = grading_standard_id
        self.hide_final_grades = hide_final_grades
        self.homeroom_course = homeroom_course
        self.id = id
        self.is_public = is_public
        self.is_public_to_auth_users = is_public_to_auth_users
        self.license = license
        self.name = name
        self.public_syllabus = public_syllabus
        self.public_syllabus_to_auth = public_syllabus_to_auth
        self.restrict_enrollments_to_course_dates = restrict_enrollments_to_course_dates
        self.root_account_id = root_account_id
        self.start_at = start_at
        self.storage_quota_mb = storage_quota_mb
        self.template = template
        self.time_zone = time_zone
        self.uuid = uuid
        self.workflow_state = workflow_state

    def save(self):
        client = MongoDBClient()
        courses_collection = client.db[self.collection_name]
        courses_collection.update_one(
            {'canvas_id': self.canvas_id},
            {'$set': self.__dict__},
            upsert=True
        )

    @staticmethod
    def get_all():
        client = MongoDBClient()
        courses_collection = client.db[Courses.collection_name]
        return list(courses_collection.find())
    
    @staticmethod
    def get_by_id(course_id):
        client = MongoDBClient()
        courses_collection = client.db[Courses.collection_name]
        return courses_collection.find_one({'course_id': course_id})
    
    @staticmethod
    def delete(course_id):
        client = MongoDBClient()
        courses_collection = client.db[Courses.collection_name]
        courses_collection.delete_one({'course_id': course_id})

    @staticmethod
    def update(course_id, updates):
        client = MongoDBClient()
        courses_collection = client.db[Courses.collection_name]
        courses_collection.update_one({'course_id': course_id}, {'$set': updates})

class Assignments():
    collection_name = 'Assignments'

    def __init__(self, canvas_id, course, name, description, due_at, points_possible, submission_types, allowed_extensions, file_ids, allowed_attempts, annotatable_attachment_id, anonymize_students, anonymous_grading, anonymous_instructor_annotations, anonymous_peer_reviews, anonymous_submissions, assignment_group_id, automatic_peer_reviews, can_duplicate, course_id, created_at, important_dates, in_closed_grading_period, intra_group_peer_reviews, is_quiz_assignment, lock_at, lock_explanation, lock_info, locked_for_user, lti_context_id, max_name_length, moderated_grading, muted, omit_from_final_grade, only_visible_to_overrides, original_assignment_id, original_assignment_name, original_course_id, original_lti_resource_link_id, original_quiz_id, peer_reviews, position, post_manually, post_to_sis, published, quiz_id, require_lockdown_browser, restrict_quantitative_data, secure_params, submissions_download_url, unlock_at, updated_at, visible_to_everyone, workflow_state):
        self.canvas_id = canvas_id
        self.course = course
        self.name = name
        self.description = description
        self.due_at = due_at
        self.points_possible = points_possible
        self.submission_types = submission_types
        self.allowed_extensions = allowed_extensions
        self.file_ids = file_ids
        self.allowed_attempts = allowed_attempts
        self.annotatable_attachment_id = annotatable_attachment_id
        self.anonymize_students = anonymize_students
        self.anonymous_grading = anonymous_grading
        self.anonymous_instructor_annotations = anonymous_instructor_annotations
        self.anonymous_peer_reviews = anonymous_peer_reviews
        self.anonymous_submissions = anonymous_submissions
        self.assignment_group_id = assignment_group_id
        self.automatic_peer_reviews = automatic_peer_reviews
        self.can_duplicate = can_duplicate
        self.course_id = course_id
        self.created_at = created_at
        self.important_dates = important_dates
        self.in_closed_grading_period = in_closed_grading_period
        self.intra_group_peer_reviews = intra_group_peer_reviews
        self.is_quiz_assignment = is_quiz_assignment
        self.lock_at = lock_at
        self.lock_explanation = lock_explanation
        self.lock_info = lock_info
        self.locked_for_user = locked_for_user
        self.lti_context_id = lti_context_id
        self.max_name_length = max_name_length
        self.moderated_grading = moderated_grading
        self.muted = muted
        self.omit_from_final_grade = omit_from_final_grade
        self.only_visible_to_overrides = only_visible_to_overrides
        self.original_assignment_id = original_assignment_id
        self.original_assignment_name = original_assignment_name
        self.original_course_id = original_course_id
        self.original_lti_resource_link_id = original_lti_resource_link_id
        self.original_quiz_id = original_quiz_id
        self.peer_reviews = peer_reviews
        self.position = position
        self.post_manually = post_manually
        self.post_to_sis = post_to_sis
        self.published = published
        self.quiz_id = quiz_id
        self.require_lockdown_browser = require_lockdown_browser
        self.restrict_quantitative_data = restrict_quantitative_data
        self.secure_params = secure_params
        self.submissions_download_url = submissions_download_url
        self.unlock_at = unlock_at
        self.updated_at = updated_at
        self.visible_to_everyone = visible_to_everyone
        self.workflow_state = workflow_state

    def save(self):
        client = MongoDBClient()
        assignments_collection = client.db[self.collection_name]
        assignments_collection.insert_one(self.__dict__)
    
    @staticmethod
    def get_all():
        client = MongoDBClient()
        assignments_collection = client.db[Assignments.collection_name]
        return list(assignments_collection.find())
    
    @staticmethod
    def get_by_id(assignment_id):
        client = MongoDBClient()
        assignments_collection = client.db[Assignments.collection_name]
        return assignments_collection.find_one({'assignment_id': assignment_id})
    
    @staticmethod
    def get_by_course_id(course_id):
        client = MongoDBClient()
        assignments_collection = client.db[Assignments.collection_name]
        return list(assignments_collection.find({'course_id': int(course_id)}))
    
    @staticmethod
    def delete(canvas_id):
        client = MongoDBClient()
        assignments_collection = client.db[Assignments.collection_name]
        assignments_collection.delete_one({'assignment_id': canvas_id})

    @staticmethod
    def update(canvas_id, updates):
        client = MongoDBClient()
        assignments_collection = client.db[Assignments.collection_name]
        assignments_collection.update_one({'assignment_id': canvas_id}, {'$set': updates})

class CustomTasks():
    collection_name = 'CustomTasks'

    def __init__(self, name, description, due_date, complete):
        self.name = name
        self.description = description
        self.due_date = due_date
        self.complete = complete

    def save(self):
        client = MongoDBClient()
        custom_tasks_collection = client.db[self.collection_name]
        custom_tasks_collection.insert_one(self.__dict__)

    @staticmethod
    def get_all():
        client = MongoDBClient()
        custom_tasks_collection = client.db[CustomTasks.collection_name]
        return list(custom_tasks_collection.find())
    
    @staticmethod
    def get_by_id(id):
        client = MongoDBClient()
        custom_tasks_collection = client.db[CustomTasks.collection_name]
        return custom_tasks_collection.find_one({'_id': id})
    
    @staticmethod
    def delete(id):
        client = MongoDBClient()
        custom_tasks_collection = client.db[CustomTasks.collection_name]
        custom_tasks_collection.delete_one({'_id': id})

    @staticmethod
    def update(id, updates):
        client = MongoDBClient()
        custom_tasks_collection = client.db[CustomTasks.collection_name]
        custom_tasks_collection.update_one({'_id': id}, {'$set': updates})

class StudentAssignments():
    collection_name = 'StudentAssignments'

    def __init__(self, student, assignment, completed, custom_tasks):
        self.student = student
        self.assignment = assignment
        self.completed = completed
        self.custom_tasks = custom_tasks

    def save(self):
        client = MongoDBClient()
        student_assignments_collection = client.db[self.collection_name]
        student_assignments_collection.insert_one(self.__dict__)

    @staticmethod
    def get_all():
        client = MongoDBClient()
        student_assignments_collection = client.db[StudentAssignments.collection_name]
        return list(student_assignments_collection.find())
    
    @staticmethod
    def get_by_id(id):
        client = MongoDBClient()
        student_assignments_collection = client.db[StudentAssignments.collection_name]
        return student_assignments_collection.find_one({'_id': id})
    
    @staticmethod
    def delete(id):
        client = MongoDBClient()
        student_assignments_collection = client.db[StudentAssignments.collection_name]
        student_assignments_collection.delete_one({'_id': id})

    @staticmethod
    def update(id, updates):
        client = MongoDBClient()
        student_assignments_collection = client.db[StudentAssignments.collection_name]
        student_assignments_collection.update_one({'_id': id}, {'$set': updates})

class Quizzes():
    collection_name = 'Quizzes'

    def __init__(self, canvas_id, course, title, description, due_at, time_limit, quiz_type, allowed_attempts, file_ids):
        self.canvas_id = canvas_id
        self.course = course
        self.title = title
        self.description = description
        self.due_at = due_at
        self.time_limit = time_limit
        self.quiz_type = quiz_type
        self.allowed_attempts = allowed_attempts
        self.file_ids = file_ids

    def save(self):
        client = MongoDBClient()
        quizzes_collection = client.db[self.collection_name]
        quizzes_collection.insert_one(self.__dict__)

    @staticmethod
    def get_all():
        client = MongoDBClient()
        quizzes_collection = client.db[Quizzes.collection_name]
        return list(quizzes_collection.find())
    
    @staticmethod
    def get_by_id(canvas_id):
        client = MongoDBClient()
        quizzes_collection = client.db[Quizzes.collection_name]
        return quizzes_collection.find_one({'canvas_id': canvas_id})
    
    @staticmethod
    def delete(canvas_id):
        client = MongoDBClient()
        quizzes_collection = client.db[Quizzes.collection_name]
        quizzes_collection.delete_one({'canvas_id': canvas_id})

    @staticmethod
    def update(canvas_id, updates):
        client = MongoDBClient()
        quizzes_collection = client.db[Quizzes.collection_name]
        quizzes_collection.update_one({'canvas_id': canvas_id}, {'$set': updates})

class Submissions():
    collection_name = 'Submissions'

    def __init__(self, canvas_id, assignment, student, submitted_at, score):
        self.canvas_id = canvas_id
        self.assignment = assignment
        self.student = student
        self.submitted_at = submitted_at
        self.score = score

    def save(self):
        client = MongoDBClient()
        submissions_collection = client.db[self.collection_name]
        submissions_collection.insert_one(self.__dict__)
    
    @staticmethod
    def get_all():
        client = MongoDBClient()
        submissions_collection = client.db[Submissions.collection_name]
        return list(submissions_collection.find())
    
    @staticmethod
    def get_by_id(canvas_id):
        client = MongoDBClient()
        submissions_collection = client.db[Submissions.collection_name]
        return submissions_collection.find_one({'canvas_id': canvas_id})
    
    @staticmethod
    def delete(canvas_id):
        client = MongoDBClient()
        submissions_collection = client.db[Submissions.collection_name]
        submissions_collection.delete_one({'canvas_id': canvas_id})

    @staticmethod
    def update(canvas_id, updates):
        client = MongoDBClient()
        submissions_collection = client.db[Submissions.collection_name]
        submissions_collection.update_one({'canvas_id': canvas_id}, {'$set': updates})

class Files():
    collection_name = 'Files'

    def __init__(self, file_id, filename, display_name, url, size, content_type, created_at, modified_at):
        self.file_id = file_id
        self.filename = filename
        self.display_name = display_name
        self.url = url
        self.size = size
        self.content_type = content_type
        self.created_at = created_at
        self.modified_at = modified_at

    def save(self):
        client = MongoDBClient()
        files_collection = client.db[self.collection_name]
        files_collection.insert_one(self.__dict__)
    
    @staticmethod
    def get_all():
        client = MongoDBClient()
        files_collection = client.db[Files.collection_name]
        return list(files_collection.find())
    
    @staticmethod
    def get_by_id(file_id):
        client = MongoDBClient()
        files_collection = client.db[Files.collection_name]
        return files_collection.find_one({'file_id': file_id})
    
    @staticmethod
    def delete(file_id):
        client = MongoDBClient()
        files_collection = client.db[Files.collection_name]
        files_collection.delete_one({'file_id': file_id})

    @staticmethod
    def update(file_id, updates):
        client = MongoDBClient()
        files_collection = client.db[Files.collection_name]
        files_collection.update_one({'file_id': file_id}, {'$set': updates})

class Deadlines():
    collection_name = 'Deadlines'

    def __init__(self, canvas_id, title, description, deadline_date):
        self.canvas_id = canvas_id
        self.title = title
        self.description = description
        self.deadline_date = deadline_date

    def save(self):
        client = MongoDBClient()
        deadlines_collection = client.db[self.collection_name]
        deadlines_collection.insert_one(self.__dict__)

    @staticmethod
    def get_all():
        client = MongoDBClient()
        deadlines_collection = client.db[Deadlines.collection_name]
        return list(deadlines_collection.find())
    
    @staticmethod
    def get_by_id(canvas_id):
        client = MongoDBClient()
        deadlines_collection = client.db[Deadlines.collection_name]
        return deadlines_collection.find_one({'canvas_id': canvas_id})
    
    @staticmethod
    def delete(canvas_id):
        client = MongoDBClient()
        deadlines_collection = client.db[Deadlines.collection_name]
        deadlines_collection.delete_one({'canvas_id': canvas_id})

    @staticmethod
    def update(canvas_id, updates):
        client = MongoDBClient()
        deadlines_collection = client.db[Deadlines.collection_name]
        deadlines_collection.update_one({'canvas_id': canvas_id}, {'$set': updates})