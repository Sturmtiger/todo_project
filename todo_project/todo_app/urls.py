from django.urls import path
from .views import *

urlpatterns = [
    path('', main, name='main_url'),
    path('project/create/', ProjectCreate.as_view(), name='create_project_url'),
    path('task/create/', TaskCreate.as_view(), name='create_task_url'),
    path('archive', archive, name='archive_url')
]