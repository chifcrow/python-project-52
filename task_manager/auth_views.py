# task_manager/auth_views.py

from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.http import HttpRequest, HttpResponse


class CustomLoginView(auth_views.LoginView):
    def form_valid(self, form) -> HttpResponse:
        response = super().form_valid(form)
        messages.success(self.request, "Вы залогинены")
        return response


class CustomLogoutView(auth_views.LogoutView):
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        response = super().post(request, *args, **kwargs)
        messages.info(request, "Вы разлогинены")
        return response
