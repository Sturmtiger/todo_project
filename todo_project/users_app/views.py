from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# from django.views.generic import View
from .forms import UserRegisterForm
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            messages.success(request, 'Your account has been created! You are now able to log in!')
            return redirect('login_url')
    else:
        form = UserRegisterForm()
    return render(request, 'users_app/register.html', {'form': form})