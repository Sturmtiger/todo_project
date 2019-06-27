from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from django.contrib import messages
from .forms import *
from datetime import datetime

class ObjectCreateMixin:
    redirect_url = None

    def post(self, request):
        if 'project_create_submit' in request.POST:
            bound_form = ProjectForm(user=request.user, data=request.POST)
            if bound_form.is_valid():
                new_project = bound_form.save(commit=False)
                new_project.user = User.objects.get(id=request.user.id)
                new_project.save()
                messages.success(request, f'Project "{new_project.name}" has been created successfully!')

            elif self.redirect_url == 'today_url':
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
                                                                       date_until__lte=timezone.localtime().replace(
                                                                           hour=23,
                                                                           minute=59,
                                                                           second=59),
                                                                       status='').count() for project in projects}

                context = {
                    'today_obj': True,
                    'redirect_url': self.redirect_url,
                    'title': 'Today',
                    'today_date': datetime.now(),
                    'projects': projects,
                    'overdue_tasks': overdue_tasks,
                    'tasks': tasks,
                    'tasks_counted': tasks_counted,
                    'project_form': bound_form,
                    'task_form': task_form,
                }
                return render(request, 'todo_app/main.html', context=context)

            elif self.redirect_url == 'today_url':
                task_form = TaskForm(user=request.user)
                projects = Project.objects.filter(user=request.user)
                tasks = Task.objects.filter(project__user=request.user,
                                            date_until__gt=timezone.localtime().replace(hour=23,
                                                                                        minute=59,
                                                                                        second=59),
                                            date_until__lte=timezone.localtime().replace(hour=23,
                                                                                         minute=59,
                                                                                         second=59) + timezone.timedelta(
                                                days=7),
                                            status='')
                tasks_counted = {
                project.name: project.task_set.filter(date_until__gt=timezone.localtime().replace(hour=23,
                                                                                                  minute=59,
                                                                                                  second=59),
                                                      date_until__lte=timezone.localtime().replace(hour=23,
                                                                                                   minute=59,
                                                                                                   second=59) + timezone.timedelta(
                                                          days=7),
                                                      status='').count() for project in projects}
                context = {
                    'next7days_obj': True,
                    'redirect_url': self.redirect_url,
                    'title': 'Next 7 days',
                    'today_date': timezone.localtime(),
                    'projects': projects,
                    'tasks': tasks,
                    'tasks_counted': tasks_counted,
                    'project_form': bound_form,
                    'task_form': task_form,
                }
                return render(request, 'todo_app/main.html', context=context)

        elif 'task_create_submit' in request.POST:
            post = request.POST.copy()
            post['date_until'] = post.get('date_until').replace('T', ' ')
            bound_form = TaskForm(request.user, post)
            if bound_form.is_valid():
                new_task = bound_form.save()
                messages.success(request, f'Task "{new_task.name}" has been created successfully!')

            elif self.redirect_url == 'today_url':
                project_form = ProjectForm()
                projects = Project.objects.filter(user=request.user)
                overdue_tasks = Task.objects.filter(project__user=request.user,
                                                    date_until__lt=timezone.localtime(),
                                                    status='')
                tasks = Task.objects.filter(project__user=request.user,  # for a day
                                            date_until__gt=timezone.localtime(),
                                            date_until__lte=timezone.localtime().replace(hour=23, minute=59, second=59),
                                            status='')
                tasks_counted = {project.name: project.task_set.filter(date_until__gt=timezone.localtime(),
                                                                       date_until__lte=timezone.localtime().replace(
                                                                           hour=23,
                                                                           minute=59,
                                                                           second=59),
                                                                       status='').count() for project in projects}

                context = {
                    'today_obj': True,
                    'redirect_url': self.redirect_url,
                    'title': 'Today',
                    'today_date': datetime.now(),
                    'projects': projects,
                    'overdue_tasks': overdue_tasks,
                    'tasks': tasks,
                    'tasks_counted': tasks_counted,
                    'project_form': project_form,
                    'task_form': bound_form,
                }
                return render(request, 'todo_app/main.html', context=context)

            elif self.redirect_url == 'next7days_url':
                project_form = ProjectForm()
                projects = Project.objects.filter(user=request.user)
                tasks = Task.objects.filter(project__user=request.user,
                                            date_until__gt=timezone.localtime().replace(hour=23,
                                                                                        minute=59,
                                                                                        second=59),
                                            date_until__lte=timezone.localtime().replace(hour=23,
                                                                                         minute=59,
                                                                                         second=59) + timezone.timedelta(
                                                days=7),
                                            status='')
                tasks_counted = {
                project.name: project.task_set.filter(date_until__gt=timezone.localtime().replace(hour=23,
                                                                                                  minute=59,
                                                                                                  second=59),
                                                      date_until__lte=timezone.localtime().replace(hour=23,
                                                                                                   minute=59,
                                                                                                   second=59) + timezone.timedelta(
                                                          days=7),
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
                    'task_form': bound_form,
                }
                return render(request, 'todo_app/main.html', context=context)

        return redirect(self.redirect_url, permanent=True)
