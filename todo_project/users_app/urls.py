from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [
    # path('', Account.as_view(), name='account_url'),
    path('register/', register, name='register_url'),
    path('login/', LoginView.as_view(template_name='users_app/login.html'), name='login_url'),
    path('logout/', LogoutView.as_view(), name='logout_url'),
]