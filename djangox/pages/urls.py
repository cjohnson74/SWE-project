from django.urls import path

from .views import HomePageView, CourseListView, AssignmentsListView, AssignmentDetailsView, AssignmentBreakdownView

urlpatterns = [
    path("", HomePageView, name="home"),
    path("courses/", CourseListView, name="courses"),
    path("courses/<str:course_id>/assignments/", AssignmentsListView, name="course_assignments"),
    path("assignments/<str:assignment_id>/", AssignmentDetailsView, name="assignment_details"),
    path("assignments/<str:assignment_id>/breakdown/", AssignmentBreakdownView, name="assignment_breakdown")
]
