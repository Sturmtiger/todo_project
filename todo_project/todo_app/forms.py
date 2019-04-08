from django import forms
from .models import *
from datetime import datetime as dt

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['colour', 'name']
        widgets = {
            'colour': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'project name', 'autofocus': 'autofocus'})
        }


class TaskForm(forms.ModelForm):
    date_until = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local',
            'min': dt.now().strftime('%Y-%m-%dT%H:%M'),  # realize jQuery
            'max': dt.now().replace(year=dt.now().year+2).strftime('%Y-%m-%dT%H:%M')  # realize jQuery
        }),
        initial=dt.now().strftime('%Y-%m-%dT%H:%M')
    )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user and Project.objects.filter(user=user).exists():
            self.fields['project'] = forms.ModelChoiceField(
                empty_label='Choose the project',
                queryset=Project.objects.filter(user=user),
                widget=forms.Select(attrs={
                    'class': 'form-control'
                })
            )
        else:
            del self.fields['project']

    class Meta:
        model = Task
        fields = ['name', 'priority', 'date_until', 'project']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'task description', 'autofocus': 'autofocus'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            # 'date_until': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            # 'project': forms.Select(attrs={'class': 'form-control'}),
        }