# djangox/pages/forms.py
from django import forms
from .models import CustomTasks, Deadlines


class CustomTaskForm(forms.ModelForm):
    class Meta:
        model = CustomTasks
        fields = ['name', 'description', 'due_date', 'complete']

class DeadlineForm(forms.ModelForm):
    class Meta:
        model = Deadlines
        fields = ['title', 'description', 'deadline_date']
