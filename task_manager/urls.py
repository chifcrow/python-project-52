# task_manager/urls.py

from django.contrib import admin
from django.urls import path

from core.views import healthz, home

urlpatterns = [
    path("", home, name="home"),
    path("healthz", healthz, name="healthz"),
    path("admin/", admin.site.urls),
]
