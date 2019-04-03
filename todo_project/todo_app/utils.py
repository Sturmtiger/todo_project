from django.shortcuts import redirect
from django.contrib.auth.models import User

class ObjectCreateMixin:
    model_form = None

    def post(self, request):
        bound_form = self.model_form(request.POST)

        if bound_form.is_valid():
            new_project = bound_form.save(commit=False)
            new_project.user = User.objects.get(id=request.user.id)
            new_project.save()
            return redirect('main_url', permanent=True)

        return redirect('main_url', permanent=True)
