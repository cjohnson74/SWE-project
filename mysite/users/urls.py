from django.urls import path
from django.contrib.auth import views as auth_views  # Import default Django auth views
from .views import home, RegisterView

# Defines URL patterns for the app.
#
# Each pattern is associated with a view, which is a Python function
# (or a class-based view) that receives a Web request and returns a Web response.
#
# 'urlpatterns' is used by Django's routing system.
urlpatterns = [
    # Home page
    # Pattern: root URL ("/")
    # View: 'home'
    path('', home, name='users-home'),

    # Registration page
    # Pattern: "/register/"
    # View: 'RegisterView'
    path('register/', RegisterView.as_view(), name='users-register'),

    # Login page
    # Pattern: "/login/"
    # View: 'LoginView' from Django's default auth views
    # Note: 'template_name' specifies the HTML file to use for this view
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),

    # Logout page
    # Pattern: "/logout/"
    # View: 'LogoutView' from Django's default auth views
    # Note: 'template_name' specifies the HTML file to use for this view
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]