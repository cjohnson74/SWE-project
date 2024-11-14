from django.urls import path
from . import views
from .views import HomePageView, CourseListView, AssignmentsListView, AssignmentDetailsView, AssignmentTasksView, StudentListView, StudentDetailView, StudentCreateView, StudentUpdateView, StudentDeleteView, QuizListView, DeadlineListView, add_custom_task, add_deadline

urlpatterns = [
    path("", HomePageView, name="home"),
    path("courses/", CourseListView, name="courses"),
    path('upload/', views.upload_file, name='upload_file'),
    path('files/', views.file_list, name='file_list'),
    path('files/delete/<int:file_id>/', views.delete_file, name='delete_file')
    path("courses/<str:course_id>/assignments/", AssignmentsListView, name="assignments"),
    path('assignment_tasks/<int:assignment_id>/', AssignmentTasksView, name='assignment_tasks'),
    path("assignments/<str:assignment_id>/", AssignmentDetailsView, name="assignment_details")
    path("add_customtask/", add_custom_task, name="add_customtask"),
    path("add_deadline/", add_deadline, name="add_deadline")
]
