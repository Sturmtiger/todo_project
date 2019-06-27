# from django.shortcuts import render, redirect, reverse
# from django.http import HttpResponse
# from datetime import datetime
# from django.utils import timezone
# from .forms import *
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


class Today(LoginRequiredMixin, ObjectCreateMixin, View):
    redirect_url = 'today_url'

    def get(self, request):
        project_form = ProjectForm()
        task_form = TaskForm(request.user)
        projects = Project.objects.filter(user=request.user)
        overdue_tasks = Task.objects.filter(project__user=request.user,
                                            date_until__lt=timezone.localtime(),
                                            status='')
        tasks = Task.objects.filter(project__user=request.user,  # for a day
                                    date_until__gt=timezone.localtime(),
                                    date_until__lte=timezone.localtime().replace(hour=23, minute=59, second=59),
                                    status='')
        tasks_counted = {project.name: project.task_set.filter(date_until__gt=timezone.localtime(),
                                                               date_until__lte=timezone.localtime().replace(hour=23,
                                                                                                            minute=59,
                                                                                                            second=59),
                                                               status='').count() for project in projects}

        context = {
            'today_obj': True,
            'redirect_url': self.redirect_url,
            'title': 'Today',
            'today_date': timezone.localtime(),
            'projects': projects,
            'overdue_tasks': overdue_tasks,
            'tasks': tasks,
            'tasks_counted': tasks_counted,
            'project_form': project_form,
            'task_form': task_form,
        }
        return render(request, 'todo_app/main.html', context=context)


class NextSevenDays(LoginRequiredMixin, ObjectCreateMixin, View):
    redirect_url = 'next7days_url'

    def get(self, request):
        project_form = ProjectForm()
        task_form = TaskForm(user=request.user)
        projects = Project.objects.filter(user=request.user)
        tasks = Task.objects.filter(project__user=request.user,
                                    date_until__gt=timezone.localtime().replace(hour=23,
                                                                                minute=59,
                                                                                second=59),
                                    date_until__lte=timezone.localtime().replace(hour=23,
                                                                                 minute=59,
                                                                                 second=59)+timezone.timedelta(days=7),
                                    status='')
        tasks_counted = {project.name: project.task_set.filter(date_until__gt=timezone.localtime().replace(hour=23,
                                                                                                           minute=59,
                                                                                                           second=59),
                                                               date_until__lte=timezone.localtime().replace(hour=23,
                                                                                                            minute=59,
                                                                                                            second=59)+timezone.timedelta(days=7),
                                                               status='').count() for project in projects}
        context = {
            'next7days_obj': True,
            'redirect_url': self.redirect_url,
            'title': 'Next 7 days',
            'today_date': timezone.localtime(),
            'projects': projects,
            'tasks': tasks,
            'tasks_counted': tasks_counted,
            'project_form': project_form,
            'task_form': task_form,
        }
        return render(request, 'todo_app/main.html', context=context)


@login_required
def project_detail(request, slug):
    user = User.objects.get(id=request.user.id)
    projects = user.project_set.all()
    project = user.project_set.get(slug=slug)
    tasks = project.task_set.all()
    context = {
        'redirect_url': 'project_detail_url',
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
        'redirect_url': 'archive_url',
        'tasks': tasks,
        'title': 'Archive'
    }
    return render(request, 'todo_app/archive.html', context=context)


@login_required
def project_delete(request, slug, redirect_url):
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        project = user.project_set.get(slug=slug)
        uncompleted_tasks = project.task_set.filter(status='').count()

        if uncompleted_tasks:
            messages.error(request, f'"{project.name}" project contains uncompleted tasks!')
            if redirect_url == 'project_detail_url':
                return redirect(project, permanent=True)    # get_absolute_url
            return redirect(redirect_url, permanent=True)

        project.delete()
        messages.success(request, f'Project "{project.name}" has been deleted successfully!')
        if redirect_url == 'project_detail_url':
            return redirect('today_url', permanent=True)
        return redirect(redirect_url, permanent=True)


@login_required
def task_delete(request, id, redirect_url):
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request, f'Task "{task.name}" has been deleted successfully!')
        if redirect_url == 'project_detail_url':
            return redirect(task.project, permanent=True)   # get_absolute_url
        return redirect(redirect_url, permanent=True)

@login_required
def task_done(request, id, redirect_url):
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        task.status = 'done'
        task.save()
        messages.success(request, f'Task "{task.name}" done! Well done!:)')
        if redirect_url == 'project_detail_url':
            return redirect(task.project, permanent=True)   # get_absolute_url
        return redirect(redirect_url, permanent=True)


class ProjectUpdate(LoginRequiredMixin, View):
    def get(self, request, slug, redirect_url):
        project = Project.objects.get(slug=slug)
        bound_form = ProjectForm(instance=project)
        context = {
            # 'redirect_url': reverse(redirect_url, kwargs={'slug': project.slug})
            'redirect_url': project.get_absolute_url() if redirect_url == 'project_detail_url'
            else reverse(redirect_url),
            'title': f'"{project.name}" Project Edit',
            'form': bound_form
        }
        return render(request, 'todo_app/update_universal.html', context=context)

    def post(self, request, slug, redirect_url):
        project = Project.objects.get(slug=slug)
        bound_form = ProjectForm(request.user, request.POST, instance=project)
        if bound_form.is_valid():
            bound_form.save()
            messages.success(request, f'Project "{project.name}" has been successfully edited!')
            if redirect_url == 'project_detail_url':
                return redirect(project)    # get_absolute_url
            return redirect(redirect_url)
        context = {
            'redirect_url': redirect_url,
            'title': f'"{project.name}" Project Edit',
            'form': bound_form
        }
        return render(request, 'todo_app/update_universal.html', context=context)


class TaskUpdate(LoginRequiredMixin, View):
    def get(self, request, id, redirect_url):
        task = Task.objects.get(id=id)
        bound_form = TaskForm(request.user, instance=task)
        context = {
            # 'redirect_url': reverse(redirect_url, kwargs={'slug': task.project.slug})
            'redirect_url': task.project.get_absolute_url() if redirect_url == 'project_detail_url'
            else reverse(redirect_url),
            'title': f'"{task.name}" Task Edit',
            'form': bound_form
        }
        return render(request, 'todo_app/update_universal.html', context=context)

    def post(self, request, id, redirect_url):
        post = request.POST.copy()
        post['date_until'] = post.get('date_until').replace('T', ' ')
        task = Task.objects.get(id=id)
        bound_form = TaskForm(request.user, post, instance=task)
        if bound_form.is_valid():
            bound_form.save()
            messages.success(request, f'Task "{task.name}" has been successfully edited!')
            if redirect_url == 'project_detail_url':
                return redirect(task.project)   # get_absolute_url
            return redirect(redirect_url)
        context = {
            'redirect_url': redirect_url,
            'title': f'"{task.name}" Task Edit',
            'form': bound_form
        }
        return render(request, 'todo_app/update_universal.html', context=context)
