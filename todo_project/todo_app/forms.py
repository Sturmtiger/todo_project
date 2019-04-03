from django import forms
from .models import *

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['colour', 'name']
        widgets = {
            'colour': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'project name', 'autofocus': 'autofocus'})
        }


class TaskForm(forms.ModelForm):
    # date_until = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M'])
    class Meta:
        model = Task
        fields = ['name', 'priority', 'date_until', 'project']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'task description', 'autofocus': 'autofocus'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'date_until': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
        }