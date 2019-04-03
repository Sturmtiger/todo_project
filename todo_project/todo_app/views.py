from django.shortcuts import render
# from django.http import HttpResponse
from datetime import datetime
from .forms import *
from django.shortcuts import redirect
from django.views.generic import View
from .utils import *
# Create your views here.


def main(request):
    if request.user.is_authenticated:
        # today_date = datetime.today().strftime("%a, %d %B")
        project_form = ProjectForm()
        task_form = TaskForm()
        user = User.objects.get(id=request.user.id)
        projects = user.project_set.all()
        tasks = [task for project in projects for task in project.task_set.all()]

        context = {
            'today_date': datetime.now(),
            'projects': projects,
            'tasks': tasks,
            'project_form': project_form,
            'task_form': task_form,
        }
        return render(request, 'todo_app/main.html', context=context)

    return redirect('login_url')


def archive(request):
    user = User.objects.get(id=request.user.id)
    projects = user.project_set.all()
    tasks = [task for project in projects for task in project.task_set.filter(status='done')]
    return render(request, 'todo_app/archive.html', context={'tasks': tasks})


class ProjectCreate(View):
    def post(self, request):
        bound_form = ProjectForm(request.POST)

        if bound_form.is_valid():
            new_project = bound_form.save(commit=False)
            new_project.user = User.objects.get(id=request.user.id)
            new_project.save()
            return redirect('main_url', permanent=True)

        return redirect('main_url', permanent=True)


class TaskCreate(ObjectCreateMixin, View):  # doesn't work(notice: datetime valid problem)
    def post(self, request):
        bound_form = TaskForm(request.POST)
        print(request.POST)
        print(request.POST.get('project'))
        print(bound_form.errors)
        if bound_form.is_valid():
            new_task = bound_form.save(commit=False)
            print(bound_form)
            return redirect('main_url', permanent=True)
        return redirect('main_url', permanent=True)


def ProjectDelete(request):
    pass


def TaskDelete(request):
    pass
