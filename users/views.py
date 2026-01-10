# users/views.py

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    TemplateView,
    UpdateView,
)

from users.forms import UserUpdateForm


class UserListView(ListView):
    model = get_user_model()
    template_name = "users/user_list.html"
    context_object_name = "users"


class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("login")


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = "users/user_update.html"
    success_url = reverse_lazy("users:list")

    def test_func(self) -> bool:
        return self.request.user.pk == self.get_object().pk

    def handle_no_permission(self):
        return super().handle_no_permission()


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = get_user_model()
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy("users:list")

    def test_func(self) -> bool:
        return self.request.user.pk == self.get_object().pk

    def handle_no_permission(self):
        return super().handle_no_permission()


class UsersPlaceholderView(TemplateView):
    template_name = "users/placeholder.html"
