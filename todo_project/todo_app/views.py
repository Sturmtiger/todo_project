from django.shortcuts import render
# from django.http import HttpResponse
from datetime import datetime
from django.utils import timezone
from .forms import *
from django.shortcuts import redirect
from django.views.generic import View
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.template.defaultfilters import register
# Create your views here.

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)



def main(request):
    return redirect('today_url')

@login_required
def today(request):
    project_form = ProjectForm()
    task_form = TaskForm(request.user)
    projects = Project.objects.filter(user=request.user)
    overdue_tasks = Task.objects.filter(project__user=request.user,
                                        date_until__lt=timezone.now(),
                                        status='')
    tasks = Task.objects.filter(project__user=request.user, #  for a day
                                date_until__gte=timezone.now(),
                                date_until__lt=timezone.now()+timezone.timedelta(days=1),
                                status='')
    tasks_counted = {project.name: project.task_set.filter(date_until__gte=timezone.now(),
                                                           date_until__lt=timezone.now()+timezone.timedelta(days=1),
                                                           status='').count() for project in projects}

    context = {
        'today_obj': True,
        'title': 'Today',
        'today_date': datetime.now(),
        'projects': projects,
        'overdue_tasks': overdue_tasks,
        'tasks': tasks,
        'tasks_counted': tasks_counted,
        'project_form': project_form,
        'task_form': task_form,
    }
    return render(request, 'todo_app/main.html', context=context)


@login_required
def nextSevenDays(request):
    project_form = ProjectForm()
    task_form = TaskForm(user=request.user)
    projects = Project.objects.filter(user=request.user)
    tasks = Task.objects.filter(project__user=request.user,
                                date_until__gte=timezone.now()+timezone.timedelta(days=1),
                                date_until__lt=timezone.now()+timezone.timedelta(days=8),
                                status='')
    tasks_counted = {project.name: project.task_set.filter(date_until__gte=timezone.now()+timezone.timedelta(days=1),
                                                           date_until__lt=timezone.now()+timezone.timedelta(days=8),
                                                           status='').count() for project in projects}
    context = {
        'next7days_obj': True,
        'title': 'Next 7 days',
        'today_date': datetime.now(),
        'projects': projects,
        'tasks': tasks,
        'tasks_counted': tasks_counted,
        'project_form': project_form,
        'task_form': task_form,
    }
    return render(request, 'todo_app/main.html', context=context)



@login_required
def projectDetail(request, slug):
    user = User.objects.get(id=request.user.id)
    projects = user.project_set.all()
    project = user.project_set.get(slug=slug)
    tasks = project.task_set.all()
    context = {
        'slug': slug,
        'title': project.name + ' PROJECT',
        'projects': projects,
        'project': project,
        'tasks': tasks}
    return render(request, 'todo_app/project.html', context=context)

@login_required
def archive(request):
    tasks = Task.objects.filter(project__user=request.user,
                                status='done')
    context = {
        'tasks': tasks,
        'title': 'Archive'
    }
    return render(request, 'todo_app/archive.html', context=context)


class ProjectCreate(LoginRequiredMixin, View):
    def post(self, request):
        bound_form = ProjectForm(user=request.user, data=request.POST)

        if bound_form.is_valid():
            new_project = bound_form.save(commit=False)
            new_project.user = User.objects.get(id=request.user.id)
            new_project.save()
            return redirect('main_url', permanent=True)

        return redirect('main_url', permanent=True)


class TaskCreate(LoginRequiredMixin, View):
    def post(self, request):
        post = request.POST.copy()
        post['date_until'] = post.get('date_until').replace('T', ' ')
        bound_form = TaskForm(request.user, post)
        if bound_form.is_valid():
            new_task = bound_form.save()
            return redirect('main_url', permanent=True)

        return redirect('main_url', permanent=True)

@login_required
def projectDelete(request, slug):
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        project = user.project_set.get(slug=slug)
        uncompleted_tasks = project.task_set.filter(status='').count()

        if uncompleted_tasks:
            messages.error(request, f'"{project.name}" project contains uncompleted tasks!')
            return redirect('main_url', permanent=True)

        project.delete()
        messages.success(request, f'Project "{project.name}" has been deleted successfully!')
        return redirect('main_url', permanent=True)

@login_required
def taskDelete(request, id):
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request, f'Task "{task.name}" has been deleted successfully!')
        return redirect('main_url', permanent=True)

@login_required
def taskDone(request, id):
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        task.status = 'done'
        task.save()
        messages.success(request, f'Task "{task.name}" done! Well done!:)')
        return redirect('main_url', permanent=True)


class projectUpdate(LoginRequiredMixin, View):
    def get(self, request, slug):
        project = Project.objects.get(slug=slug)
        bound_form = ProjectForm(instance=project)
        context = {
            'project': f'"{project.name}" Project Edit',
            'form': bound_form
        }
        return render(request, 'todo_app/update_universal.html', context=context)

    def post(self, request, slug):
        project = Project.objects.get(slug=slug)
        bound_form = ProjectForm(request.user, request.POST, instance=project)
        if bound_form.is_valid():
            bound_form.save()
            return redirect('main_url')
        context = {
            'project': project.name,
            'form': bound_form
        }
        return render(request, 'todo_app/update_universal.html', context=context)


class taskUpdate(LoginRequiredMixin, View):
    def get(self, request, id):
        task = Task.objects.get(id=id)
        bound_form = TaskForm(request.user, instance=task)
        context = {
            'project': f'"{task.name}" Task Edit',
            'form': bound_form
        }
        return render(request, 'todo_app/update_universal.html', context=context)

    def post(self, request, id):
        post = request.POST.copy()
        post['date_until'] = post.get('date_until').replace('T', ' ')
        task = Task.objects.get(id=id)
        bound_form = TaskForm(request.user, post, instance=task)
        if bound_form.is_valid():
            bound_form.save()
            return redirect('main_url')
        context = {
            'project': f'"{task.name}" Project Edit',
            'form': bound_form
        }
        return render(request, 'todo_app/update_universal.html', context=context)
