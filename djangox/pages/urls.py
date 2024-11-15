from django.urls import path
from . import views
from .views import HomePageView, CourseListView, AssignmentsListView, AssignmentDetailsView, AssignmentBreakdownView, AssignmentTasksView, StudentListView, StudentDetailView, StudentCreateView, StudentUpdateView, StudentDeleteView, QuizListView, DeadlineListView, add_deadline, CoursesGraphView

urlpatterns = [
    path("", HomePageView, name="home"),
    path("courses/", CourseListView, name="courses"),
    path("courses/graph/", CoursesGraphView, name="courses_graph"),
    path("courses/<str:course_id>/assignments/", AssignmentsListView, name="course_assignments"),
    path("assignments/<str:assignment_id>/breakdown/", AssignmentBreakdownView, name="assignment_breakdown"),
    path('upload/', views.upload_file, name='upload_file'),
    path('files/', views.file_list, name='file_list'),
    path('files/delete/<int:file_id>/', views.delete_file, name='delete_file'), 
    path('assignment_tasks/<int:assignment_id>/', AssignmentTasksView, name='assignment_tasks'),
    path("assignments/<str:assignment_id>/", AssignmentDetailsView, name="assignment_details"),
    path("add_deadline/", add_deadline, name="add_deadline")
]
