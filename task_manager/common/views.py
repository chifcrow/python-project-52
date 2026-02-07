from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "index.html"


def healthz(request: HttpRequest) -> HttpResponse:
    return HttpResponse("ok")
