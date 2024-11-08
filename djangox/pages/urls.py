from django.urls import path

from .views import HomePageView, CourseListView, AssignmentsListView, AssignmentDetailsView, AssignmentTasksView

urlpatterns = [
    path("", HomePageView, name="home"),
    path("courses/", CourseListView, name="courses"),
    path("courses/<str:course_id>/assignments/", AssignmentsListView, name="assignments"),
    path('assignment_tasks/<int:assignment_id>/', AssignmentTasksView, name='assignment_tasks'),
    path("assignments/<str:assignment_id>/", AssignmentDetailsView, name="assignment_details")
]
