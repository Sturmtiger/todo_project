from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from django.contrib import messages
from .forms import *
from datetime import datetime
from abc import ABCMeta, abstractmethod


class ObjectCreateMixin(metaclass=ABCMeta):
    redirect_url = None

    @abstractmethod
    def context_method(self, request, project_bound_form=None, task_bound_form=None):
        pass

    def post(self, request):
        if 'project_create_submit' in request.POST:
            project_bound_form = ProjectForm(user=request.user, data=request.POST)
            if project_bound_form.is_valid():
                new_project = project_bound_form.save(commit=False)
                new_project.user = User.objects.get(id=request.user.id)
                new_project.save()
                messages.success(request, f'Project "{new_project.name}" has been created successfully!')
            else:
                return render(request, 'todo_app/main.html', context=self.context_method(request, project_bound_form=project_bound_form))

        elif 'task_create_submit' in request.POST:
            post = request.POST.copy()
            post['date_until'] = post.get('date_until').replace('T', ' ')
            task_bound_form = TaskForm(request.user, post)
            if task_bound_form.is_valid():
                new_task = task_bound_form.save()
                messages.success(request, f'Task "{new_task.name}" has been created successfully!')
            else:
                return render(request, 'todo_app/main.html', context=self.context_method(request, task_bound_form=task_bound_form))

        return redirect(self.redirect_url, permanent=True)
