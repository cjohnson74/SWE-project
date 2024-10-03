# -*- coding: utf-8 -*-
"""
Users
-----

Provides views for handling user login, registration, and home view.
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.views import LoginView

from .forms import RegisterForm, LoginForm


def home(request):
    """Render the homepage.

    :param request: The request object.
    """
    return render(request, 'users/home.html')


class RegisterView(View):
    """
    Class-based view for User Registration.

    :param request: The request object.

    Display the register form on GET request.
    On POST request, validate the form, save the user and redirect to home if valid, else display form with errors.
    """
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        """Handle the dispatch for the view.

        :param request: The request object.
        """
        if request.user.is_authenticated:
            return redirect(to='/')

        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Handle GET requests for the view.

        :param request: The request object.
        """
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """Handle POST requests for the view.

        :param request: The request object.
        """
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='/')

        return render(request, self.template_name, {'form': form})


class CustomLoginView(LoginView):
    """
    Custom Login View that handles user login.

    :param request: The request object.

    Inherits from Django's built-in LoginView. If the user selected 'remember me', keep the session alive.
    """
    form_class = LoginForm

    def form_valid(self, form):
        """Check if the form is valid.

        :param form: The form object.
        """
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            self.request.session.set_expiry(0)

            self.request.session.modified = True

        return super(CustomLoginView, self).form_valid(form)