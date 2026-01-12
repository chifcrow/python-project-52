# tasks/views.py

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from tasks.filters import TaskFilter
from tasks.forms import TaskForm
from tasks.models import Task


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    filterset_class = TaskFilter

    def get_filterset(self, filterset_class):
        filterset = super().get_filterset(filterset_class)
        filterset.request = self.request
        return filterset


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Task created successfully.")
        return response


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_update.html"
    success_url = reverse_lazy("tasks:list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Task updated successfully.")
        return response


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("tasks:list")

    def test_func(self) -> bool:
        return self.request.user.pk == self.get_object().author_id

    def handle_no_permission(self):
        messages.error(self.request, "Only the author can delete this task.")
        return HttpResponseRedirect(reverse("tasks:list"))

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Task deleted successfully.")
        return response
