# task_manager/urls.py

from django.contrib import admin
from django.urls import include, path

from task_manager.auth_views import CustomLoginView, CustomLogoutView
from task_manager.common.views import HomeView, healthz

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("healthz", healthz, name="healthz"),
    path("users/", include("users.urls", namespace="users")),
    path("statuses/", include("statuses.urls", namespace="statuses")),
    path("tasks/", include("tasks.urls", namespace="tasks")),
    path("labels/", include("labels.urls", namespace="labels")),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(next_page="home"), name="logout"),
    path("admin/", admin.site.urls),
]
