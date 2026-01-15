# task_manager/urls.py

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.http import HttpRequest, HttpResponse
from django.urls import include, path

from core.views import HomeView, healthz


def rollbar_error(request: HttpRequest) -> HttpResponse:
    try:
        import rollbar

        rollbar.report_message("Rollbar test message from Django", level="error")
        raise RuntimeError("Rollbar test error")
    except RuntimeError:
        try:
            import rollbar

            rollbar.report_exc_info()
        except Exception:
            pass
        raise


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("healthz", healthz, name="healthz"),
    path("users/", include("users.urls", namespace="users")),
    path("statuses/", include("statuses.urls", namespace="statuses")),
    path("tasks/", include("tasks.urls", namespace="tasks")),
    path("labels/", include("labels.urls", namespace="labels")),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="home"),
        name="logout",
    ),
    path("debug/rollbar-error/", rollbar_error, name="rollbar_error"),
    path("admin/", admin.site.urls),
]
