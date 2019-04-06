from django.urls import path
from .views import *

urlpatterns = [
    path('', main, name='main_url'),
    path('archive/', archive, name='archive_url'),
    path('project/<str:slug>/detail/', projectDetail, name='project_detail_url'),
    path('project/create/', ProjectCreate.as_view(), name='create_project_url'),
    path('project/<str:slug>/delete/', projectDelete, name='project_delete_url'),
    path('task/create/', TaskCreate.as_view(), name='create_task_url'),
    path('task/<int:id>/delete/', taskDelete, name='task_delete_url'),
    path('task/<int:id>/done/', taskDone, name='task_done_url')

]