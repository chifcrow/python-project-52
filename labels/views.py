# labels/views.py

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from labels.forms import LabelForm
from labels.models import Label


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = "labels/label_list.html"
    context_object_name = "labels"


class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/label_form.html"
    success_url = reverse_lazy("labels:list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Метка успешно создана.")
        return response


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/label_update.html"
    success_url = reverse_lazy("labels:list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Метка успешно изменена.")
        return response


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = "labels/label_confirm_delete.html"
    success_url = reverse_lazy("labels:list")

    def form_valid(self, form):
        label = self.get_object()
        if label.task_set.exists():
            messages.error(
                self.request,
                "Невозможно удалить метку, потому что она используется.",
            )
            return HttpResponseRedirect(reverse("labels:list"))

        response = super().form_valid(form)
        messages.success(self.request, "Метка успешно удалена.")
        return response
