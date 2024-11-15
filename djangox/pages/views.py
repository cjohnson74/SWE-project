from .forms import DeadlineForm
from .models import Students, Courses, Assignments, Quizzes, StudentAssignments, Submissions, Files, Deadlines, AssignmentBreakdown, YouTubeResource, AssignmentBreakdownTask
from .forms import fileForm
from .models import fileModel
from django.shortcuts import redirect, render, get_object_or_404
from .claude_service import get_assignment_breakdown
from django.http import HttpResponse, JsonResponse
from django.template import loader
import json
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
    assignment = get_object_or_404(Assignments, assignment_id=assignment_id)
    existing_breakdown = None
    
    # Check for existing breakdown
    try:
        existing_breakdown = AssignmentBreakdown.objects.get(assignment=assignment)
        if existing_breakdown:
            # Format existing breakdown data
            breakdown = {
                'total_estimated_time': existing_breakdown.total_estimated_time,
                'work_distribution': existing_breakdown.work_distribution,
                'breaks_and_buffer': existing_breakdown.breaks_and_buffer,
                'assignment_breakdown': []
            }
            
            # Add tasks to the breakdown
            for task in existing_breakdown.tasks.all():
                task_data = {
                    'task_number': task.task_number,
                    'description': task.description,
                    'estimated_time': task.estimated_time,
                    'due_date': task.due_date.isoformat(),
                    'completed': task.completed,
                    'tips': task.tips,
                    'priority': task.priority,
                    'distraction_mitigation': task.distraction_mitigation,
                    'focus_techniques': task.focus_techniques,
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
        breakdown = None

    if request.method == 'POST':
        try:
            # Fetch the breakdown from the Claude API
            breakdown = get_assignment_breakdown(assignment_id)
            print("Breakdown:", breakdown)

            # Get the assignment object
            assignment = get_object_or_404(Assignments, assignment_id=assignment_id)

            # Delete existing breakdowns for this assignment
            AssignmentBreakdown.objects.filter(assignment=assignment).delete()

            # Create a new breakdown
            assignment_breakdown = AssignmentBreakdown.objects.create(
                assignment=assignment,
                total_estimated_time=breakdown['total_estimated_time'],
                work_distribution=breakdown['work_distribution'],
                breaks_and_buffer=breakdown['breaks_and_buffer']
            )

            # Save tasks and YouTube resources
            for task_data in breakdown['assignment_breakdown']:
                task = AssignmentBreakdownTask.objects.create(
                    breakdown=assignment_breakdown,
                    task_number=task_data['task_number'],
                    description=task_data['description'],
                    estimated_time=task_data['estimated_time'],
                    due_date=task_data['due_date'],
                    completed=False,
                    tips=task_data.get('tips', ''),
                    priority=task_data['priority'],
                    distraction_mitigation=task_data.get('distraction_mitigation', ''),
                    focus_techniques=task_data.get('focus_techniques', ''),
                    reward=task_data.get('reward', '')
                )

                # Save YouTube resources for the task
                for resource in task_data.get('youtube_resources', []):
                    YouTubeResource.objects.create(
                        task=task,
                        title=resource['title'],
                        link=resource['link']
                    )

            return JsonResponse(breakdown)
        except Exception as e:
            print("Error fetching breakdown:", e)
            return JsonResponse({'error': str(e)}, status=400)

    return render(request, 'pages/assignment_breakdown.html', {
        'assignment_id': assignment_id,
        'breakdown': breakdown,
        'has_existing_breakdown': breakdown is not None
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
        'assignments__assignment_breakdown__tasks',  # Prefetch AssignmentBreakdown for each Assignment
        'assignments__assignment_breakdown__tasks__youtube_resources'  # Prefetch YouTubeResources for each AssignmentBreakdownTask
    ).all()

    courses_data = []
    for course in courses:
        course_info = {
            'course_id': course.course_id,
            'name': course.name,
            'course_code': course.course_code,
            'assignments': []
        }

        for assignment in course.assignments.all():
            if assignment.due_at is None:
                due_at = ""
            else:
                due_at = assignment.due_at.isoformat()
            assignment_info = {
                'name': assignment.name,
                'due_at': due_at,
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

    return render(request, 'pages/courses_graph.html', {'courses': courses_data})