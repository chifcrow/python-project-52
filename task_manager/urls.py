# task_manager/urls.py

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from core.views import HomeView, healthz
from users.forms import CustomAuthenticationForm

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("healthz", healthz, name="healthz"),
    path("users/", include("users.urls", namespace="users")),
    path("statuses/", include("statuses.urls", namespace="statuses")),
    path("tasks/", include("tasks.urls", namespace="tasks")),
    path("labels/", include("labels.urls", namespace="labels")),
    path(
        "login/",
        auth_views.LoginView.as_view(
            authentication_form=CustomAuthenticationForm
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="home"),
        name="logout",
    ),
    path("admin/", admin.site.urls),
]
