from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.admin.sites import AdminSite
from .admin import CustomUserAdmin


class CustomUserTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )
        self.superuser = get_user_model().objects.create_superuser(
            username='adminuser',
            email='admin@example.com',
            password='adminpassword123'
        )

    def test_create_user(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertTrue(self.user.check_password('testpassword123'))

    def test_create_superuser(self):
        self.assertTrue(self.superuser.is_superuser)
        self.assertTrue(self.superuser.is_staff)

    def test_str_method(self):
        self.assertEqual(str(self.user), 'testuser@example.com')


class CustomUserFormsTests(TestCase):
    def test_valid_custom_user_creation_form(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'password123',
            'password2': 'password123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_custom_user_creation_form(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'password123',
            'password2': 'wrongpassword',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_custom_user_change_form(self):
        user = get_user_model().objects.create_user(
            username='changetest',
            email='changetest@example.com',
            password='testpassword123'
        )
        form = CustomUserChangeForm(instance=user, data={
            'username': 'changeduser',
            'email': 'changeduser@example.com',
        })
        self.assertTrue(form.is_valid())


class MockRequest:
    user = None


class CustomUserAdminTests(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.user_admin = CustomUserAdmin(get_user_model(), self.site)
        self.user = get_user_model().objects.create_user(
            username='adminusertest',
            email='adminusertest@example.com',
            password='adminpassword123'
        )

    def test_list_display(self):
        self.assertEqual(self.user_admin.list_display, ['email', 'username'])

    def test_model_in_admin(self):
        self.assertEqual(self.user_admin.model, get_user_model())

    def test_get_queryset(self):
        request = MockRequest()
        queryset = self.user_admin.get_queryset(request)
        self.assertIn(self.user, queryset)
