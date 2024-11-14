from .forms import CustomTaskForm, DeadlineForm
from .models import Students, Courses, Assignments, Quizzes, StudentAssignments, Submissions, Files, CustomTasks, Deadlines
from django.shortcuts import redirect, render, get_object_or_404
from .claude_service import get_assignment_breakdown
from django.http import HttpResponse
from django.template import loader

def HomePageView(request):
    template = loader.get_template('pages/home.html')
    return HttpResponse(template.render({}, request))

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
    course = Courses.objects.get(course_id=course_id)
    assignments = Assignments.objects.filter(course=course)
    template = loader.get_template('pages/course_assignments.html')
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

# Custom Task Views
def CustomTaskListView(request):
    custom_tasks = CustomTasks.objects.all()
    template = loader.get_template('pages/customtask_list.html')
    return HttpResponse(template.render({'custom_tasks': custom_tasks}, request))

def CustomTaskDetailView(request):
    custom_task = CustomTasks.objects.get(canvas_id=request.GET.get('canvas_id'))
    template = loader.get_template('pages/customtask_detail.html')
    return HttpResponse(template.render({'custom_task': custom_task}, request))

def CustomTaskCreateView(request):
    CustomTasks.objects.create(request.POST)
    return redirect('customtask_list')

def CustomTaskUpdateView(request):
    CustomTasks.objects.update(request.POST)
    return redirect('customtask_list')

def CustomTaskDeleteView(request):
    CustomTasks.objects.delete(request.GET.get('canvas_id'))
    return redirect('customtask_list')

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
    breakdown = None
    # student_id = request.user.id  # Uncomment if you need to use student ID

    if request.method == 'POST':
        try:
            breakdown = get_assignment_breakdown(assignment_id)
            print("Breakdown:", JsonResponse(breakdown))
            return JsonResponse(breakdown)
        except Exception as e:
            print("Error fetching breakdown:", e)
            return JsonResponse({'error': str(e)}, status=400)

    return render(request, 'pages/assignment_breakdown.html', {'assignment_id': assignment_id, 'breakdown': breakdown})

def add_custom_task(request):
    if request.method == 'POST':
        form = CustomTaskForm(request.POST)
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
        form = CustomTaskForm()  # Create a new empty form

    template = loader.get_template('pages/customtask_form.html')
    return HttpResponse(template.render({'form': form}, request))

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

# def course_detail(request, course_id):
#     """View to display details of a specific course."""
#     course = get_object_or_404(Courses.get_all(), cou=course_id)  # Fetch the course by ID
#     return render(request, 'pages/course_detail.html', {'course': course})