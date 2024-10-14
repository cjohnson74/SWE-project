from django.http import JsonResponse
from django import forms
from .models import Students, Courses, Assignments, Quizzes, StudentAssignments, Submissions, Files, CustomTasks, Deadlines
from django.shortcuts import redirect, render, get_object_or_404

def HomePageView(request):
    return render(request, 'pages/home.html')

def AboutPageView(request):
    return render(request, 'pages/about.html')

def QuizListView(request):
    quizzes = Quizzes.get_all()
    return render(request, 'pages/quiz_list.html', {'quizzes': quizzes})


def AssignmentListView(request):
    assignments = Assignments.get_all()
    return render(request, 'pages/assignment_list.html', {'assignments': assignments})


def DeadlineListView(request):
    deadlines = Deadlines.get_all()
    return render(request, 'pages/deadline_list.html', {'deadlines': deadlines})

# Student Views
def StudentListView(request):
    students = Students.get_all()
    return render(request, 'pages/student_list.html', {'students': students})

def StudentDetailView(request):
    student = Students.get_by_id(request.GET.get('canvas_id'))
    return render(request, 'pages/student_detail.html', {'student': student})

def StudentCreateView(request):
    Students.create(request.POST)
    return redirect('student_list')

def StudentUpdateView(request):
    Students.update(request.POST)
    return redirect('student_list')

def StudentDeleteView(request):
    Students.delete(request.GET.get('canvas_id'))
    return redirect('student_list')

# Course Views
def CourseListView(request):
    courses = Courses.get_all()
    return render(request, 'pages/courses.html', {'courses': courses})

def CourseDetailView(request, course_id):
    course = Courses.get_by_id(int(course_id))
    return render(request, 'pages/course_detail.html', {'course': course})

def CourseCreateView(request):
    Courses.create(request.POST)
    return redirect('course_list')

def CourseUpdateView(request):
    Courses.update(request.POST)
    return redirect('course_list')

def CourseDeleteView(request):
    Courses.delete(request.GET.get('canvas_id'))
    return redirect('course_list')

# Assignment Views
def AssignmentsListView(request, course_id):
    course = Courses.get_by_id(course_id)
    assignments = Assignments.get_by_course_id(course_id)
    return render(request, 'pages/course_assignments.html', {'course': course, 'assignments': assignments})

def AssignmentDetailsView(request, assignment_id):
    assignment = Assignments.get_by_id(int(assignment_id))
    course = Courses.get_by_id(assignment['course_id'])
    return render(request, 'pages/assignment_details.html', {'course': course, 'assignment': assignment})

def AssignmentCreateView(request):
    Assignments.create(request.POST)
    return redirect('assignment_list')

def AssignmentUpdateView(request):
    Assignments.update(request.POST)
    return redirect('assignment_list')

def AssignmentDeleteView(request):
    Assignments.delete(request.GET.get('canvas_id'))
    return redirect('assignment_list')

# Student Assignment Views
def StudentAssignmentListView(request):
    student_assignments = StudentAssignments.get_all()
    return render(request, 'pages/student_assignment_list.html', {'student_assignments': student_assignments})

def StudentAssignmentDetailView(request):
    student_assignment = StudentAssignments.get_by_id(request.GET.get('canvas_id'))
    return render(request, 'pages/student_assignment_detail.html', {'student_assignment': student_assignment})

def StudentAssignmentCreateView(request):
    StudentAssignments.create(request.POST)
    return redirect('student_assignment_list')

def StudentAssignmentUpdateView(request):
    StudentAssignments.update(request.POST)
    return redirect('student_assignment_list')

def StudentAssignmentDeleteView(request):
    StudentAssignments.delete(request.GET.get('canvas_id'))
    return redirect('student_assignment_list')

# Quiz Views
def QuizListView(request):
    quizzes = Quizzes.get_all()
    return render(request, 'pages/quiz_list.html', {'quizzes': quizzes})

def QuizDetailView(request):
    quiz = Quizzes.get_by_id(request.GET.get('canvas_id'))
    return render(request, 'pages/quiz_detail.html', {'quiz': quiz})

def QuizCreateView(request):
    Quizzes.create(request.POST)
    return redirect('quiz_list')

def QuizUpdateView(request):
    Quizzes.update(request.POST)
    return redirect('quiz_list')

def QuizDeleteView(request):
    Quizzes.delete(request.GET.get('canvas_id'))
    return redirect('quiz_list')

# Submission Views
def SubmissionListView(request):
    submissions = Submissions.get_all()
    return render(request, 'pages/submission_list.html', {'submissions': submissions})

def SubmissionDetailView(request):
    submission = Submissions.get_by_id(request.GET.get('canvas_id'))
    return render(request, 'pages/submission_detail.html', {'submission': submission})

def SubmissionCreateView(request):
    Submissions.create(request.POST)
    return redirect('submission_list')

def SubmissionUpdateView(request):
    Submissions.update(request.POST)
    return redirect('submission_list')

def SubmissionDeleteView(request):
    Submissions.delete(request.GET.get('canvas_id'))
    return redirect('submission_list')

# File Views
def FileListView(request):
    files = Files.get_all()
    return render(request, 'pages/file_list.html', {'files': files})

def FileDetailView(request):
    file = Files.get_by_id(request.GET.get('canvas_id'))
    return render(request, 'pages/file_detail.html', {'file': file})

def FileUploadView(request):
    Files.create(request.POST)
    return redirect('file_list')

def FileUpdateView(request):
    Files.update(request.POST)
    return redirect('file_list')

def FileDeleteView(request):
    Files.delete(request.GET.get('canvas_id'))
    return redirect('file_list')

# Custom Task Views
def CustomTaskListView(request):
    custom_tasks = CustomTasks.get_all()
    return render(request, 'pages/customtask_list.html', {'custom_tasks': custom_tasks})

def CustomTaskDetailView(request):
    custom_task = CustomTasks.get_by_id(request.GET.get('canvas_id'))
    return render(request, 'pages/customtask_detail.html', {'custom_task': custom_task})

def CustomTaskCreateView(request):
    CustomTasks.create(request.POST)
    return redirect('customtask_list')

def CustomTaskUpdateView(request):
    CustomTasks.update(request.POST)
    return redirect('customtask_list')

def CustomTaskDeleteView(request):
    CustomTasks.delete(request.GET.get('canvas_id'))
    return redirect('customtask_list')

# Deadline Views
def DeadlineListView(request):
    deadlines = Deadlines.get_all()
    return render(request, 'pages/deadline_list.html', {'deadlines': deadlines})

def DeadlineDetailView(request):
    deadline = Deadlines.get_by_id(request.GET.get('canvas_id'))
    return render(request, 'pages/deadline_detail.html', {'deadline': deadline})

def DeadlineCreateView(request):
    Deadlines.create(request.POST)
    return redirect('deadline_list')

def DeadlineUpdateView(request):
    Deadlines.update(request.POST)
    return redirect('deadline_list')

def DeadlineDeleteView(request):
    Deadlines.delete(request.GET.get('canvas_id'))
    return redirect('deadline_list')

def add_custom_task(request):
    if request.method == 'POST':
        form = forms.CustomTaskForm(request.POST)
        if form.is_valid():
            # Create a new CustomTask instance and save it to MongoDB
            new_task = CustomTasks(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                due_date=form.cleaned_data['due_date'],
                complete=form.cleaned_data.get('complete', False)
            )
            new_task.save()  # Save to MongoDB
            return redirect('customtask_list')  # Redirect to the custom task list after adding
    else:
        form = forms.CustomTaskForm()  # Create a new empty form

    return render(request, 'pages/customtask_form.html', {'form': form})

def add_deadline(request):
    if request.method == 'POST':
        form = forms.DeadlineForm(request.POST)
        if form.is_valid():
            new_deadline = Deadlines(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                deadline_date=form.cleaned_data['deadline_date']
            )
            new_deadline.save()
            return redirect('deadline_list')
    else:
        form = forms.DeadlineForm()

    return render(request, 'pages/deadline_form.html', {'form': form})

# def course_detail(request, course_id):
#     """View to display details of a specific course."""
#     course = get_object_or_404(Courses.get_all(), cou=course_id)  # Fetch the course by ID
#     return render(request, 'pages/course_detail.html', {'course': course})