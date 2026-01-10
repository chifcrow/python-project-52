# task_manager/urls.py

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from core.views import HomeView, healthz

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("healthz", healthz, name="healthz"),
    path("users/", include("users.urls", namespace="users")),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="home"),
        name="logout",
    ),
    path("admin/", admin.site.urls),
]
