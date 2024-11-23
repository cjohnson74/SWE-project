# djangox/pages/forms.py
from django import forms
from .models import Deadlines, fileModel, AssignmentFile

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class fileForm(forms.ModelForm):
    class Meta:
        model = fileModel
        fields = ['file']

class DeadlineForm(forms.ModelForm):
    class Meta:
        model = Deadlines
        fields = ['title', 'description', 'deadline_date']

class AssignmentFileForm(forms.Form):
    files = MultipleFileField(
        widget=MultipleFileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.doc,.docx,.txt,.jpg,.jpeg,.png,.gif,.bmp',
            'id': 'fileInput'
        }),
        required=False
    )
