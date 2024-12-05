from .forms import DeadlineForm
from .models import Students, Courses, Assignments, Quizzes, StudentAssignments, Submissions, Files, Deadlines, AssignmentBreakdown, YouTubeResource, AssignmentBreakdownTask, AssignmentFile, generate_embeddings, Modules, ModuleItems
from .forms import fileForm, AssignmentFileForm
from .models import fileModel
from django.shortcuts import redirect, render, get_object_or_404
from .claude_service import get_assignment_breakdown, get_assignment_files_content
from django.http import HttpResponse, JsonResponse
from django.template import loader
import json
from django.utils import timezone
import logging
from django.views.decorators.http import require_http_methods
from django.utils.dateparse import parse_datetime
from django.core.files.storage import default_storage
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .embedding_service import EmbeddingService
from datetime import datetime

logger = logging.getLogger(__name__)

def LoginPageView(request):
    return render(request, 'account/login.html')

def HomePageView(request):
    courses = Courses.objects.all()
    return render(request, 'pages/home.html', {'courses': courses})

def AboutPageView(request):
    template = loader.get_template('pages/about.html')
    return HttpResponse(template.render({}, request))

def QuizListView(request):
    quizzes = Quizzes.objects.all()
    template = loader.get_template('pages/quiz_list.html')
    return HttpResponse(template.render({'quizzes': quizzes}, request))

def AssignmentListView(request):
    assignments = Assignments.objects.all()
    template = loader.get_template('pages/assignment_list.html')
    return HttpResponse(template.render({'assignments': assignments}, request))

def DeadlineListView(request):
    deadlines = Deadlines.objects.all()
    template = loader.get_template('pages/deadline_list.html')
    return HttpResponse(template.render({'deadlines': deadlines}, request))

# Student Views
def StudentListView(request):
    students = Students.objects.all()
    template = loader.get_template('pages/student_list.html')
    return HttpResponse(template.render({'students': students}, request))

def StudentDetailView(request):
    student = Students.objects.get(canvas_id=request.GET.get('canvas_id'))
    template = loader.get_template('pages/student_detail.html')
    return HttpResponse(template.render({'student': student}, request))

def StudentCreateView(request):
    Students.objects.create(request.POST)
    return redirect('student_list')

def StudentUpdateView(request):
    Students.objects.update(request.POST)
    return redirect('student_list')

def StudentDeleteView(request):
    Students.objects.delete(request.GET.get('canvas_id'))
    return redirect('student_list')

# Course Views
def CourseListView(request):
    courses = Courses.objects.all()
    template = loader.get_template('pages/courses.html')
    return HttpResponse(template.render({'courses': courses}, request))

def CourseDetailView(request, course_id):
    course = Courses.objects.get(course_id=course_id)
    template = loader.get_template('pages/course_detail.html')
    return HttpResponse(template.render({'course': course}, request))

def CourseCreateView(request):
    Courses.objects.create(request.POST)
    return redirect('course_list')

def CourseUpdateView(request):
    Courses.objects.update(request.POST)
    return redirect('course_list')

def CourseDeleteView(request):
    Courses.objects.delete(request.GET.get('canvas_id'))
    return redirect('course_list')

def AssignmentsListView(request, course_id):
    print(f"Requested course_id: {course_id}")
    course = Courses.objects.get(course_id=course_id)
    print(f"Retrieved course: {course}")
    assignments = Assignments.objects.filter(course=course)
    template = loader.get_template('pages/assignments.html')
    return HttpResponse(template.render({'course': course, 'assignments': assignments}, request))

def AssignmentDetailsView(request, assignment_id):
    assignment = Assignments.objects.get(assignment_id=assignment_id)
    course = course=assignment.course
    template = loader.get_template('pages/assignment_details.html')
    return HttpResponse(template.render({'course': course, 'assignment': assignment}, request))

def AssignmentCreateView(request):
    Assignments.objects.create(request.POST)
    return redirect('assignment_list')

def AssignmentUpdateView(request):
    Assignments.objects.update(request.POST)
    return redirect('assignment_list')

def AssignmentDeleteView(request):
    Assignments.objects.delete(request.GET.get('canvas_id'))
    return redirect('assignment_list')

def AssignmentTasksView(request, assignment_id):
    return render(request, 'pages/assignment_tasks.html', {'assignment_id': assignment_id})

# Student Assignment Views
def StudentAssignmentListView(request):
    student_assignments = StudentAssignments.objects.all()
    template = loader.get_template('pages/student_assignment_list.html')
    return HttpResponse(template.render({'student_assignments': student_assignments}, request))

def StudentAssignmentDetailView(request):
    student_assignment = StudentAssignments.objects.get(canvas_id=request.GET.get('canvas_id'))
    template = loader.get_template('pages/student_assignment_detail.html')
    return HttpResponse(template.render({'student_assignment': student_assignment}, request))

def StudentAssignmentCreateView(request):
    StudentAssignments.objects.create(request.POST)
    return redirect('student_assignment_list')

def StudentAssignmentUpdateView(request):
    StudentAssignments.objects.update(request.POST)
    return redirect('student_assignment_list')

def StudentAssignmentDeleteView(request):
    StudentAssignments.objects.delete(request.GET.get('canvas_id'))
    return redirect('student_assignment_list')

# Quiz Views
def QuizListView(request):
    quizzes = Quizzes.objects.all()
    template = loader.get_template('pages/quiz_list.html')
    return HttpResponse(template.render({'quizzes': quizzes}, request))

def QuizDetailView(request):
    quiz = Quizzes.objects.get(canvas_id=request.GET.get('canvas_id'))
    template = loader.get_template('pages/quiz_detail.html')
    return HttpResponse(template.render({'quiz': quiz}, request))

def QuizCreateView(request):
    Quizzes.objects.create(request.POST)
    return redirect('quiz_list')

def QuizUpdateView(request):
    Quizzes.objects.update(request.POST)
    return redirect('quiz_list')

def QuizDeleteView(request):
    Quizzes.objects.delete(request.GET.get('canvas_id'))
    return redirect('quiz_list')

# Submission Views
def SubmissionListView(request):
    submissions = Submissions.objects.all()
    template = loader.get_template('pages/submission_list.html')
    return HttpResponse(template.render({'submissions': submissions}, request))

def SubmissionDetailView(request):
    submission = Submissions.objects.get(canvas_id=request.GET.get('canvas_id'))
    template = loader.get_template('pages/submission_detail.html')
    return HttpResponse(template.render({'submission': submission}, request))

def SubmissionCreateView(request):
    Submissions.objects.create(request.POST)
    return redirect('submission_list')

def SubmissionUpdateView(request):
    Submissions.objects.update(request.POST)
    return redirect('submission_list')

def SubmissionDeleteView(request):
    Submissions.objects.delete(request.GET.get('canvas_id'))
    return redirect('submission_list')

# File Views
def FileListView(request):
    files = Files.objects.all()
    template = loader.get_template('pages/file_list.html')
    return HttpResponse(template.render({'files': files}, request))

def FileDetailView(request):
    file = Files.objects.get(canvas_id=request.GET.get('canvas_id'))
    template = loader.get_template('pages/file_detail.html')
    return HttpResponse(template.render({'file': file}, request))

def FileUploadView(request):
    Files.objects.create(request.POST)
    return redirect('file_list')

def FileUpdateView(request):
    Files.objects.update(request.POST)
    return redirect('file_list')

def FileDeleteView(request):
    Files.objects.delete(request.GET.get('canvas_id'))
    return redirect('file_list')

# Deadline Views
def DeadlineListView(request):
    deadlines = Deadlines.objects.all()
    template = loader.get_template('pages/deadline_list.html')
    return HttpResponse(template.render({'deadlines': deadlines}, request))

def DeadlineDetailView(request):
    deadline = Deadlines.objects.get(canvas_id=request.GET.get('canvas_id'))
    template = loader.get_template('pages/deadline_detail.html')
    return HttpResponse(template.render({'deadline': deadline}, request))

def DeadlineCreateView(request):
    Deadlines.objects.create(request.POST)
    return redirect('deadline_list')

def DeadlineUpdateView(request):
    Deadlines.objects.update(request.POST)
    return redirect('deadline_list')

def DeadlineDeleteView(request):
    Deadlines.objects.delete(request.GET.get('canvas_id'))
    return redirect('deadline_list')

def AssignmentBreakdownView(request, assignment_id):
    logger.debug(f"Processing assignment breakdown for ID: {assignment_id}")

    try:
        assignment = Assignments.objects.get(assignment_id=assignment_id)
    except Assignments.DoesNotExist:
        logger.error(f"Assignment with ID {assignment_id} not found")

    if request.method == "POST":
        try:
            # Get new breakdown from Claude
            breakdown_data = get_assignment_breakdown(assignment_id)
            logger.debug("Received breakdown data from Claude")

            # Delete existing breakdown if it exists
            AssignmentBreakdown.objects.filter(assignment=assignment).delete()

            # Create new AssignmentBreakdown
            new_breakdown = AssignmentBreakdown.objects.create(
                assignment=assignment,
                initial_assessment=breakdown_data['analysis']['thought_process']['initial_assessment'],
                complexity_evaluation=breakdown_data['analysis']['thought_process']['complexity_evaluation'],
                complexity_scores=breakdown_data['analysis']['thought_process']['complexity_scores'],
                key_requirements='\n'.join(breakdown_data['analysis']['thought_process']['key_requirements']),
                potential_challenges='\n'.join(breakdown_data['analysis']['thought_process']['potential_challenges']),
                skill_level_considerations=breakdown_data['analysis']['thought_process']['skill_level_considerations'],
                total_estimated_time=breakdown_data['total_estimated_time'],
                work_distribution=breakdown_data['work_distribution'],
                breaks_and_buffer=breakdown_data['breaks_and_buffer'],
                reasoning=breakdown_data.get('reasoning', ''),
                progress_tracking=breakdown_data.get('progress_tracking', ''),
                time_management='\n'.join(breakdown_data['adhd_specific_strategies']['time_management']),
                focus_impprovement='\n'.join(breakdown_data['adhd_specific_strategies']['focus_improvement']),
                motivation_boosters='\n'.join(breakdown_data['adhd_specific_strategies']['motivation_boosters']),
                milestone_rewards='\n'.join(breakdown_data['reward_system']['milestone_rewards']),
                completion_reward=breakdown_data['reward_system']['completion_reward'],
                progress_visualization=breakdown_data['reward_system']['progress_visualization']
            )

            # Create tasks with proper date formatting
            for task_data in breakdown_data['assignment_breakdown']:
                # Convert the due_date string to a proper datetime object
                try:
                    # If due_date is just a date string, append a default time
                    due_date_str = task_data['due_date']
                    if 'T' not in due_date_str:
                        due_date_str += 'T23:59:59Z'
                    due_date = parse_datetime(due_date_str)
                    if not due_date:
                        due_date = timezone.now()  # Fallback to current time if parsing fails
                except (KeyError, ValueError):
                    due_date = timezone.now()  # Fallback to current time if there's an error

                task = AssignmentBreakdownTask.objects.create(
                    breakdown=new_breakdown,
                    task_number=task_data['task_number'],
                    title=task_data['title'],
                    description=task_data['description'],
                    estimated_time=task_data['estimated_time'],
                    due_date=due_date,  # Use the parsed datetime
                    tips=task_data.get('tips', ''),
                    priority=task_data.get('priority', 'medium'),
                    potential_distractions=','.join(task_data.get('potential_distractions', [])),
                    distraction_mitigation=task_data.get('distraction_mitigation', ''),
                    focus_techniques=','.join(task_data.get('focus_techniques', [])),
                    reward=task_data.get('reward', '')
                )

                # Create YouTube resources
                for resource_data in task_data.get('youtube_resources', []):
                    YouTubeResource.objects.create(
                        task=task,
                        title=resource_data['title'],
                        link=resource_data['link']
                    )

            return JsonResponse({'status': 'success'})

        except Exception as e:
            logger.error(f"Error creating breakdown: {str(e)}", exc_info=True)
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    # Handle GET request
    try:
        # First try to get the assignment breakdown
        try:
            existing_breakdown = AssignmentBreakdown.objects.select_related('assignment').prefetch_related('tasks__youtube_resources').get(assignment=assignment)
            logger.debug(f"Found existing breakdown for assignment: {assignment.name}")
            has_existing_breakdown = True

            # Find the next task to focus on
            next_task = None
            current_time = timezone.now()
            incomplete_tasks = existing_breakdown.tasks.filter(completed=False).order_by('due_date')

            if incomplete_tasks.exists():
                next_task = incomplete_tasks.first()
                logger.debug(f"Found next task: {next_task.task_number} - {next_task.description}")

            # Convert stored data back into the expected format
            breakdown = {
                'analysis': {
                    'thought_process': {
                        'initial_assessment': existing_breakdown.initial_assessment,
                        'complexity_evaluation': existing_breakdown.complexity_evaluation,
                        'complexity_scores': existing_breakdown.complexity_scores,
                        'key_requirements': existing_breakdown.key_requirements.split('\n') if existing_breakdown.key_requirements else [],
                        'potential_challenges': existing_breakdown.potential_challenges.split('\n') if existing_breakdown.potential_challenges else [],
                        'skill_level_considerations': existing_breakdown.skill_level_considerations
                    }
                },
                'total_estimated_time': existing_breakdown.total_estimated_time,
                'work_distribution': existing_breakdown.work_distribution,
                'breaks_and_buffer': existing_breakdown.breaks_and_buffer,
                'reasoning': existing_breakdown.reasoning,
                'progress_tracking': existing_breakdown.progress_tracking,
                'adhd_specific_strategies': {
                    'time_management': existing_breakdown.time_management.split('\n') if existing_breakdown.time_management else [],
                    'focus_improvement': existing_breakdown.focus_impprovement.split('\n') if existing_breakdown.focus_impprovement else [],
                    'motivation_boosters': existing_breakdown.motivation_boosters.split('\n') if existing_breakdown.motivation_boosters else []
                },
                'reward_system': {
                    'milestone_rewards': existing_breakdown.milestone_rewards.split('\n') if existing_breakdown.milestone_rewards else [],
                    'completion_reward': existing_breakdown.completion_reward,
                    'progress_visualization': existing_breakdown.progress_visualization
                },
                'assignment_breakdown': [],
                'next_task': {
                    'task_number': next_task.task_number,
                    'title': next_task.title,
                    'description': next_task.description,
                    'estimated_time': next_task.estimated_time,
                    'due_date': next_task.due_date,
                    'tips': next_task.tips,
                    'youtube_resources': [
                        {
                            'title': resource.title,
                            'link': resource.link
                        } for resource in next_task.youtube_resources.all()
                    ]
                } if next_task else None,
                'additional_resources': [
                    {
                        'title': resource.title,
                        'link': resource.link
                    } for task in existing_breakdown.tasks.all()
                    for resource in task.youtube_resources.all()
                ]
            }

            # Add tasks to the breakdown
            for task in existing_breakdown.tasks.all():
                task_data = {
                    'task_number': task.task_number,
                    'title': task.title,
                    'description': task.description,
                    'estimated_time': task.estimated_time,
                    'due_date': task.due_date,
                    'completed': task.completed,
                    'tips': task.tips,
                    'priority': task.priority,
                    'potential_distractions': task.potential_distractions.split(',') if task.potential_distractions else [],
                    'distraction_mitigation': task.distraction_mitigation,
                    'focus_techniques': task.focus_techniques.split(',') if task.focus_techniques else [],
                    'reward': task.reward,
                    'youtube_resources': [
                        {
                            'title': resource.title,
                            'link': resource.link
                        } for resource in task.youtube_resources.all()
                    ]
                }
                breakdown['assignment_breakdown'].append(task_data)

        except AssignmentBreakdown.DoesNotExist:
            logger.debug(f"No existing breakdown found for assignment: {assignment.name}")
            has_existing_breakdown = False
            breakdown = {
                'analysis': None,
                'assignment_breakdown': [],
                'next_task': None,
                'additional_resources': [],
                'reasoning': None,
                'progress_tracking': None,
                'adhd_specific_strategies': {
                    'time_management': [],
                    'focus_improvement': [],
                    'motivation_boosters': []
                },
                'reward_system': {
                    'milestone_rewards': [],
                    'completion_reward': None,
                    'progress_visualization': None
                }
            }
            logger.debug("Created empty breakdown structure")

        # Add debug logging for template context
        logger.debug(f"Template context - has_existing_breakdown: {has_existing_breakdown}")
        logger.debug(f"Template context - analysis present: {'analysis' in breakdown}")
        logger.debug(f"Template context - number of tasks: {len(breakdown.get('assignment_breakdown', []))}")

        return render(request, 'pages/assignment_breakdown.html', {
            'assignment_id': assignment_id,
            'assignment': assignment,
            'breakdown': breakdown,
            'has_existing_breakdown': has_existing_breakdown,
            'analysis': breakdown.get('analysis'),
            'tasks': breakdown.get('assignment_breakdown', []),
            'next_task': breakdown.get('next_task'),
            'additional_resources': breakdown.get('additional_resources', []),
            'reasoning': breakdown.get('reasoning'),
            'progress_tracking': breakdown.get('progress_tracking'),
            'adhd_specific_strategies': breakdown.get('adhd_specific_strategies', {}),
            'reward_system': breakdown.get('reward_system', {})
        })

    except Exception as e:
        logger.error(f"Error processing assignment breakdown: {str(e)}")
        return render(request, 'pages/assignment_breakdown.html', {
            'assignment_id': assignment_id,
            'assignment': assignment,
            'has_existing_breakdown': False,
            'error_message': "An error occurred while loading the assignment breakdown."
        })

def add_deadline(request):
    if request.method == 'POST':
        form = DeadlineForm(request.POST)
        if form.is_valid():
            new_deadline = Deadlines(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                deadline_date=form.cleaned_data['deadline_date']
            )
            new_deadline.save()
            return redirect('deadline_list')
    else:
        form = DeadlineForm()

    template = loader.get_template('pages/deadline_form.html')
    return HttpResponse(template.render({'form': form}, request))

def upload_file(request):
    if request.method == 'POST':
        form = fileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the uploaded file
            form = fileForm()  # Reset the form after a successful upload
            return render(request, 'pages/upload.html', {'form': form, 'success': True})
    else:
        form = fileForm()

    return render(request, 'pages/upload.html', {'form': form})

def delete_file(request, file_id):
    file_instance = fileModel.objects.get(id=file_id)

    # Delete the file from the file system
    file_instance.file.delete()

    # Delete the database record
    file_instance.delete()

    return redirect('file_list')

def file_list(request):
    files = fileModel.objects.all()
    return render(request, 'pages/file_list.html', {'files': files})

def CoursesGraphView(request):
    courses = Courses.objects.prefetch_related(
        'assignments__assignment_breakdown__tasks'
    ).all()

    # Get current datetime for comparison
    current_time = timezone.now()

    # Find the next assignment due
    next_assignment = None
    earliest_due_date = None

    for course in courses:
        for assignment in course.assignments.all():
            if assignment.due_at:  # Check if due date exists
                # Only consider assignments that aren't completed and aren't overdue
                if assignment.due_at > current_time:
                    if earliest_due_date is None or assignment.due_at < earliest_due_date:
                        earliest_due_date = assignment.due_at
                        next_assignment = assignment

    courses_data = []
    for course in courses:
        course_info = {
            'course_id': course.course_id,
            'name': course.name,
            'course_code': course.course_code,
            'assignments': [],
            'next_assignment': 'none'  # Add this field
        }

        for assignment in course.assignments.all():
            if assignment.due_at is None:
                due_at = ""
            else:
                due_at = assignment.due_at.isoformat()

            # Calculate if this is the next assignment due
            is_next = 'true' if (next_assignment and assignment.id == next_assignment.id) else 'false'

            assignment_info = {
                'name': assignment.name,
                'due_at': due_at,
                'is_next': is_next,  # Add this field
                'breakdowns': []
            }

            for breakdown in assignment.assignment_breakdown.all():
                breakdown_info = {
                    'total_estimated_time': breakdown.total_estimated_time,
                    'work_distribution': breakdown.work_distribution,
                    'breaks_and_buffer': breakdown.breaks_and_buffer,
                    'tasks': []
                }

                for task in breakdown.tasks.all():
                    task_info = {
                        'task_number': task.task_number,
                        'title': task.title,
                        'description': task.description,
                        'estimated_time': task.estimated_time,
                        'due_date': task.due_date.isoformat(),
                        'youtube_resources': []
                    }

                    for resource in task.youtube_resources.all():
                        task_info['youtube_resources'].append({
                            'title': resource.title,
                            'link': resource.link
                        })

                    breakdown_info['tasks'].append(task_info)

                assignment_info['breakdowns'].append(breakdown_info)

            course_info['assignments'].append(assignment_info)

        courses_data.append(course_info)

    return render(request, 'pages/courses_graph.html', {
        'courses': courses_data,
        'next_assignment': {
            'name': next_assignment.name,
            'course': next_assignment.course.name,
            'due_at': next_assignment.due_at.isoformat()
        } if next_assignment else None
    })

@require_http_methods(["POST"])
def save_progress(request, assignment_id):
    try:
        data = json.loads(request.body)
        # Try to get assignment without raising 404
        try:
            assignment = Assignments.objects.get(assignment_id=assignment_id)
        except Assignments.DoesNotExist:
            logger.error(f"Assignment with ID {assignment_id} not found")

        breakdown = AssignmentBreakdown.objects.get(assignment=assignment)

        # Update progress tracking
        breakdown.progress_tracking = f"Completed {data['completed_count']} out of {data['total_count']} tasks"
        breakdown.save()

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@require_http_methods(["POST"])
def save_task_status(request, task_number):
    try:
        data = json.loads(request.body)
        assignment_id = data.get('assignment_id')
        completed = data.get('completed', False)

        # Get the task
        try:
            assignment = Assignments.objects.get(assignment_id=assignment_id)
        except Assignments.DoesNotExist:
            logger.error(f"Assignment with ID {assignment_id} not found")

        breakdown = AssignmentBreakdown.objects.get(assignment=assignment)
        task = AssignmentBreakdownTask.objects.get(
            breakdown=breakdown,
            task_number=task_number
        )

        # Update task completion status
        task.completed = completed
        task.save()

        # Update overall progress tracking
        total_tasks = breakdown.tasks.count()
        completed_tasks = breakdown.tasks.filter(completed=True).count()
        breakdown.progress_tracking = f"Completed {completed_tasks} out of {total_tasks} tasks"
        breakdown.save()

        return JsonResponse({
            'status': 'success',
            'completed': completed,
            'progress': {
                'completed': completed_tasks,
                'total': total_tasks
            }
        })
    except Exception as e:
        logger.error(f"Error saving task status: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

def upload_assignment_file(request, assignment_id):
    if request.method == 'POST':
        try:
            assignment = Assignments.objects.get(assignment_id=assignment_id)
            form = AssignmentFileForm(request.POST, request.FILES)

            if form.is_valid():
                files = form.cleaned_data['files']
                uploaded_files = []

                for file in files:
                    # Create the AssignmentFile instance
                    assignment_file = AssignmentFile.objects.create(
                        assignment=assignment,
                        file=file,
                        file_name=file.name,
                        file_type=file.name.split('.')[-1].lower()
                    )
                    
                    # Extract content using Claude first
                    try:
                        content = get_assignment_files_content(assignment)
                        # if content and len(content) > 0:
                        #     # Update the file with Claude's response
                        #     print(f"🔍 Claude's response: {content}")
                        #     assignment_file.claude_response = content[0]
                        #     assignment_file.save()
                            
                            # # Queue embedding generation as a background task
                            # generate_embeddings.delay(assignment_file.id)
                    except Exception as e:
                        logger.error(f"Error processing file content: {str(e)}")
                    
                    uploaded_files.append({
                        'id': assignment_file.id,
                        'name': assignment_file.file_name,
                        'category': assignment_file.file_category,
                        'embedding_status': 'pending'
                    })

                return JsonResponse({
                    'status': 'success',
                    'message': 'Files uploaded successfully',
                    'files': uploaded_files
                })

            return JsonResponse({
                'status': 'error',
                'message': form.errors
            }, status=400)

        except Exception as e:
            logger.error(f"Error uploading files: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': f'Upload failed: {str(e)}'
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)

def delete_assignment_file(request, assignment_id, file_id):
    if request.method == 'POST':
        try:
            file = AssignmentFile.objects.get(id=file_id, assignment__assignment_id=assignment_id)
            file.delete()
            return JsonResponse({
                'status': 'success',
                'message': 'File deleted successfully',
                'redirect_url': request.META.get('HTTP_REFERER')
            })
        except AssignmentFile.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'File not found'
            }, status=404)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)

@api_view(['POST'])
def semantic_search(request, assignment_id):
    try:
        print(f"\n🔍 Starting semantic search for assignment {assignment_id}")
        query = request.data.get('query')
        if not query:
            return Response({'error': 'No query provided'}, status=400)
            
        print(f"📝 Query: {query}")
        embedding_service = EmbeddingService()
        files = AssignmentFile.objects.filter(
            assignment_id=assignment_id,
            last_embedded__isnull=False  # Only get files with completed embeddings
        )
        print(f"📁 Found {files.count()} files with embeddings")
        
        if not files.exists():
            return Response({
                'status': 'warning',
                'message': 'Files are still being processed. Please try again in a moment.',
                'results': []
            })
        
        results = []
        for file in files:
            if file.chunk_embeddings:
                print(f"\n📄 Searching in file: {file.file_name}")
                similar_chunks = embedding_service.find_similar_chunks(
                    query=query,
                    chunk_embeddings=file.chunk_embeddings,
                    top_k=3
                )
                
                for similarity, chunk, index in similar_chunks:
                    print(f"  ✓ Found match (similarity: {similarity:.3f})")
                    results.append({
                        'file_name': file.file_name,
                        'chunk': chunk,
                        'similarity': float(similarity),
                        'chunk_index': index
                    })
            else:
                print(f"⚠️ No embeddings found for file: {file.file_name}")
        
        # Sort by similarity
        results.sort(key=lambda x: x['similarity'], reverse=True)
        top_results = results[:5]  # Return top 5 results
        
        print(f"\n✅ Search complete - found {len(top_results)} top results")
        return Response({
            'status': 'success',
            'results': top_results
        })
        
    except Exception as e:
        print(f"❌ Error during semantic search: {str(e)}")
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=500)

@api_view(['GET'])
def check_embeddings_status(request, assignment_id):
    try:
        total_files = AssignmentFile.objects.filter(assignment_id=assignment_id).count()
        processed_files = AssignmentFile.objects.filter(
            assignment_id=assignment_id,
            last_embedded__isnull=False
        ).count()
        
        return Response({
            'status': 'success',
            'total_files': total_files,
            'processed_files': processed_files,
            'is_complete': total_files == processed_files
        })
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=500)

def ModuleListView(request, course_id):
    """Display modules and their items for a course"""
    course = get_object_or_404(Courses, course_id=course_id)
    modules = Modules.objects.filter(course=course).prefetch_related('items')
    
    context = {
        'course': course,
        'modules': modules
    }
    return render(request, 'pages/module_list.html', context)
