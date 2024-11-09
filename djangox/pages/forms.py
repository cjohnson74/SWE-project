# djangox/pages/forms.py
from django import forms
from .models import fileModel

class CustomTaskForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea)
    due_date = forms.DateField()
    complete = forms.BooleanField(required=False)

class DeadlineForm(forms.Form):
    title = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea)
    deadline_date = forms.DateField()

class fileForm(forms.ModelForm):
    class Meta:
        model = fileModel
        fields = ['file']