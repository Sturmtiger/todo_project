from django.urls import path
from .views import *

urlpatterns = [
    path('', main, name='main_url'),
    path('today/', Today.as_view(), name='today_url'),
    path('next-7-days/', NextSevenDays.as_view(), name='next7days_url'),
    path('archive/', archive, name='archive_url'),
    path('project/<str:slug>/detail/', project_detail, name='project_detail_url'),
    path('project/<str:slug>/update/<str:redirect_url>/', ProjectUpdate.as_view(), name='project_update_url'),
    path('task/<int:id>/update/<str:redirect_url>/', TaskUpdate.as_view(), name='task_update_url'),
    path('project/<str:slug>/delete/<str:redirect_url>/', project_delete, name='project_delete_url'),
    path('task/<str:id>/delete/<str:redirect_url>/', task_delete, name='task_delete_url'),
    path('task/<int:id>/done/<str:redirect_url>/', task_done, name='task_done_url')
]