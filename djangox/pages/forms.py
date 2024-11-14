# djangox/pages/forms.py
from django import forms
from .models import CustomTasks, Deadlines, fileModel

class CustomTaskForm(forms.ModelForm):
    class Meta:
        model = CustomTasks
        fields = ['name', 'description', 'due_date', 'complete']

class fileForm(forms.ModelForm):
    class Meta:
        model = fileModel
        fields = ['file']

class DeadlineForm(forms.ModelForm):
    class Meta:
        model = Deadlines
        fields = ['title', 'description', 'deadline_date']
