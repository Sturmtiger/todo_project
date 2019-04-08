from django.shortcuts import render
# from django.http import HttpResponse
from datetime import datetime
from django.utils import timezone
from .forms import *
from django.shortcuts import redirect
from django.views.generic import View
from .utils import *
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def main(request):
    return redirect('today_url')


def today(request):
    if request.user.is_authenticated:
        # today_date = datetime.today().strftime("%a, %d %B")
        project_form = ProjectForm()
        task_form = TaskForm(user=request.user)
        projects = Project.objects.filter(user=request.user)
        overdue_tasks = Task.objects.filter(project__user=request.user,
                                            date_until__lt=timezone.now(),
                                            status='')
        tasks = Task.objects.filter(project__user=request.user, #  for a day
                                    date_until__gte=timezone.now(),
                                    date_until__lt=timezone.now()+timezone.timedelta(days=1))

        context = {
            'today_obj': True,
            'title': 'Today',
            'today_date': datetime.now(),
            'projects': projects,
            'overdue_tasks': overdue_tasks,
            'tasks': tasks,
            'project_form': project_form,
            'task_form': task_form,
        }
        return render(request, 'todo_app/main.html', context=context)

    return redirect('login_url')


def nextSevenDays(request):
    if request.user.is_authenticated:
        # today_date = datetime.today().strftime("%a, %d %B")
        project_form = ProjectForm()
        task_form = TaskForm(user=request.user)
        projects = Project.objects.filter(user=request.user)
        tasks = Task.objects.filter(project__user=request.user, #  for next 7 days
                                    date_until__gte=timezone.now()+timezone.timedelta(days=1),
                                    date_until__lt=timezone.now()+timezone.timedelta(days=8))

        context = {
            'next7days_obj': True,
            'title': 'Today',
            'today_date': datetime.now(),
            'projects': projects,
            'tasks': tasks,
            'project_form': project_form,
            'task_form': task_form,
        }
        return render(request, 'todo_app/main.html', context=context)

    return redirect('login_url')


def projectDetail(request, slug):
    user = User.objects.get(id=request.user.id)
    project = user.project_set.get(slug=slug)
    tasks = project.task_set.all()
    context = {
        'title' : project.name,
        'project': project,
        'tasks': tasks}
    return render(request, 'todo_app/project.html', context=context)

@login_required
def archive(request):
    user = User.objects.get(id=request.user.id)
    projects = user.project_set.all()
    tasks = [task for project in projects for task in project.task_set.filter(status='done')]
    return render(request, 'todo_app/archive.html', context={'tasks': tasks, 'title': 'Archive'})


class ProjectCreate(View):
    def post(self, request):
        bound_form = ProjectForm(request.POST)

        if bound_form.is_valid():
            new_project = bound_form.save(commit=False)
            new_project.user = User.objects.get(id=request.user.id)
            new_project.save()
            return redirect('main_url', permanent=True)

        return redirect('main_url', permanent=True)


class TaskCreate(View):
    def post(self, request):
        post = request.POST.copy()
        post['date_until'] = post.get('date_until').replace('T', ' ')
        bound_form = TaskForm(request.user, post)
        if bound_form.is_valid():
            new_task = bound_form.save()
            return redirect('main_url', permanent=True)

        return redirect('main_url', permanent=True)


def projectDelete(request, slug):
    print(request.user)
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


def taskDelete(request, id):
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request, f'Task <b>"{task.name}"</b> has been deleted successfully!')
        return redirect('main_url', permanent=True)

def taskDone(request, id):
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        task.status = 'done'
        task.save()
        return redirect('main_url', permanent=True)