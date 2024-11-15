# djangox/pages/forms.py
from django import forms
from .models import Deadlines, fileModel

class fileForm(forms.ModelForm):
    class Meta:
        model = fileModel
        fields = ['file']

class DeadlineForm(forms.ModelForm):
    class Meta:
        model = Deadlines
        fields = ['title', 'description', 'deadline_date']
