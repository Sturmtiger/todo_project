from django import forms
from .models import *
from datetime import datetime as dt
from django.core.exceptions import ValidationError
from django.utils import timezone



class ProjectForm(forms.ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = Project
        fields = ['colour', 'name']
        widgets = {
            'colour': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'project name', 'autofocus': 'autofocus'})
        }

    def clean_name(self):
        new_project = self.cleaned_data['name']
        if Project.objects.filter(user=self.user, name__iexact=new_project).count():
            raise ValidationError('Project name must be unique!')
        return new_project

    def clean_colour(self):
        new_colour = self.cleaned_data['colour']
        if Project.objects.filter(user=self.user, colour=new_colour).count():
            raise ValidationError('Project colour must be unique!')
        return new_colour


class TaskForm(forms.ModelForm):
    date_until = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local',
            'min': dt.now().strftime('%Y-%m-%dT00:00'),
            'max': dt.now().replace(year=dt.now().year+2, day=dt.now().day+1).strftime('%Y-%m-%dT00:00')  # until 2 years
        }),
        initial=dt.now().strftime('%Y-%m-%dT00:00')
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
        }

    def clean_date_until(self):
        new_date_until = self.cleaned_data['date_until']
        print(new_date_until < timezone.now())
        if new_date_until < timezone.now() or new_date_until > timezone.now().replace(year=timezone.now().year+2):
            raise ValidationError('Datetime values error. Notice: 2 years is maximum!')
        return new_date_until