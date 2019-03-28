from django.shortcuts import render
from django.http import HttpResponse

from datetime import datetime
# Create your views here.
def main(request):
    today_date = datetime.today().strftime("%a, %d %B")
    return render(request, 'todo_app/todo_app.html', context={'today_date': today_date})