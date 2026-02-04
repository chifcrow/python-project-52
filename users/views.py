# users/views.py

from __future__ import annotations

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from users.forms import CustomUserCreationForm, UserUpdateForm


def ensure_user_names(user) -> None:
    first = (user.first_name or "").strip()
    last = (user.last_name or "").strip()
    if first or last:
        return

    username = (user.username or "").strip()
    if not username:
        return

    parts = username.replace("-", " ").replace("_", " ").strip().split()
    if not parts:
        return

    user.first_name = parts[0].title()
    user.last_name = " ".join(parts[1:]).title()
    user.save(update_fields=["first_name", "last_name"])


class UserListView(ListView):
    model = get_user_model()
    template_name = "users/user_list.html"
    context_object_name = "users"


class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Пользователь успешно зарегистрирован")
        return response


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = "users/user_update.html"
    success_url = reverse_lazy("users:list")

    def get_object(self, queryset=None):
        user = super().get_object(queryset=queryset)
        ensure_user_names(user)
        return user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Пользователь успешно изменен")
        return response

    def test_func(self) -> bool:
        return self.request.user.pk == self.get_object().pk

    def handle_no_permission(self):
        messages.error(
            self.request,
            "У вас нет прав для изменения другого пользователя.",
        )
        return HttpResponseRedirect(reverse("users:list"))


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = get_user_model()
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy("users:list")

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        # Add message before delete to survive logout/session changes.
        messages.success(request, "Пользователь успешно удален")
        return super().post(request, *args, **kwargs)

    def test_func(self) -> bool:
        return self.request.user.pk == self.get_object().pk

    def handle_no_permission(self):
        messages.error(
            self.request,
            "У вас нет прав для изменения другого пользователя.",
        )
        return HttpResponseRedirect(reverse("users:list"))
