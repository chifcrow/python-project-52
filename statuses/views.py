# statuses/views.py

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.deletion import ProtectedError
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from statuses.forms import StatusForm
from statuses.models import Status


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses/status_list.html"
    context_object_name = "statuses"


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/status_form.html"
    success_url = reverse_lazy("statuses:list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Status created successfully.")
        return response


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/status_update.html"
    success_url = reverse_lazy("statuses:list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Status updated successfully.")
        return response


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = "statuses/status_confirm_delete.html"
    success_url = reverse_lazy("statuses:list")

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                "Cannot delete status because it is in use.",
            )
            return HttpResponseRedirect(reverse("statuses:list"))
        messages.success(self.request, "Status deleted successfully.")
        return response
