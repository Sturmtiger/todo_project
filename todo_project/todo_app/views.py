from django.shortcuts import render
# from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth.models import User
from .models import *
# Create your views here.
def main(request):
    today_date = datetime.today().strftime("%a, %d %B")

    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        projects = user.project_set.all()
        tasks = [task for project in projects for task in project.task_set.all()]

        context = {
            'today_date': today_date,
            'projects': projects,
            'tasks': tasks
        }
        return render(request, 'todo_app/todo_app.html', context=context)

    return render(request, 'todo_app/todo_app.html')