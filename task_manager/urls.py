# task_manager/urls.py

from django.contrib import admin
from django.urls import path

from core.views import HomeView, healthz

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("healthz", healthz, name="healthz"),
    path("admin/", admin.site.urls),
]
