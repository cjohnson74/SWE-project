from django.test import TestCase
from django.urls import reverse, resolve
from .views import (
    HomePageView,
    CourseListView,
    CoursesGraphView,
    AssignmentsListView,
    AssignmentBreakdownView,
    AssignmentDetailsView,
    AssignmentTasksView,
    add_deadline,
    upload_file,
    file_list,
    delete_file,
)


class URLTests(TestCase):
    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, HomePageView)

    def test_courses_url_resolves(self):
        url = reverse('courses')
        self.assertEqual(resolve(url).func, CourseListView)

    def test_courses_graph_url_resolves(self):
        url = reverse('courses_graph')
        self.assertEqual(resolve(url).func, CoursesGraphView)

    def test_course_assignments_url_resolves(self):
        url = reverse('course_assignments', kwargs={'course_id': '123'})
        self.assertEqual(resolve(url).func, AssignmentsListView)

    def test_assignment_details_url_resolves(self):
        url = reverse('assignment_details', kwargs={'assignment_id': 'abc'})
        self.assertEqual(resolve(url).func, AssignmentDetailsView)

    def test_assignment_breakdown_url_resolves(self):
        url = reverse('assignment_breakdown', kwargs={'assignment_id': 'abc'})
        self.assertEqual(resolve(url).func, AssignmentBreakdownView)

    def test_assignment_tasks_url_resolves(self):
        url = reverse('assignment_tasks', kwargs={'assignment_id': 1})
        self.assertEqual(resolve(url).func, AssignmentTasksView)

    def test_add_deadline_url_resolves(self):
        url = reverse('add_deadline')
        self.assertEqual(resolve(url).func, add_deadline)

    def test_upload_file_url_resolves(self):
        url = reverse('upload_file')
        self.assertEqual(resolve(url).func, upload_file)

    def test_file_list_url_resolves(self):
        url = reverse('file_list')
        self.assertEqual(resolve(url).func, file_list)

    def test_delete_file_url_resolves(self):
        url = reverse('delete_file', kwargs={'file_id': 1})
        self.assertEqual(resolve(url).func, delete_file)


class ViewTests(TestCase):
    def test_home_page_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')  # Replace with your template name if different.

    def test_courses_page_view(self):
        response = self.client.get(reverse('courses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses_list.html')  # Replace with your template name.

    def test_courses_graph_view(self):
        response = self.client.get(reverse('courses_graph'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses_graph.html')  # Replace with your template name.

    def test_add_deadline_view(self):
        response = self.client.post(reverse('add_deadline'), {
            'title': 'Test Deadline',
            'date': '2024-12-31',
        })
        self.assertEqual(response.status_code, 200)  # Adjust based on expected behavior.

    # Add more detailed view tests here for each view.

