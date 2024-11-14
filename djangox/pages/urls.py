from django.urls import path
from .views import HomePageView, CourseListView, AssignmentsListView, AssignmentDetailsView, StudentListView, StudentDetailView, StudentCreateView, StudentUpdateView, StudentDeleteView, QuizListView, DeadlineListView, add_custom_task, add_deadline
from . import views

urlpatterns = [
    path("", HomePageView, name="home"),
    path("courses/", CourseListView, name="courses"),
    path("courses/<str:course_id>/assignments/", AssignmentsListView, name="course_assignments"),
    path("assignments/<str:assignment_id>/", AssignmentDetailsView, name="assignment_details"),
    path('upload/', views.upload_file, name='upload_file'),
    path('files/', views.file_list, name='file_list'),
    path('files/delete/<int:file_id>/', views.delete_file, name='delete_file')
    path("add_customtask/", add_custom_task, name="add_customtask"),
    path("add_deadline/", add_deadline, name="add_deadline")
]
