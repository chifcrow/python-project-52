from django.http import HttpRequest, HttpResponse
from django.views import View


class HomeView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse("Hello from Task Manager!")


def healthz(request: HttpRequest) -> HttpResponse:
    return HttpResponse("ok")
