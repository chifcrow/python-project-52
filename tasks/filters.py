# tasks/filters.py

import django_filters
from django import forms
from django.contrib.auth import get_user_model

from labels.models import Label
from statuses.models import Status
from tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        label="Статус",
        queryset=Status.objects.all().order_by("id"),
        empty_label="---------",
    )
    executor = django_filters.ModelChoiceFilter(
        label="Исполнитель",
        queryset=get_user_model().objects.all().order_by("id"),
        empty_label="---------",
    )
    labels = django_filters.ModelChoiceFilter(
        label="Метка",
        field_name="labels",
        queryset=Label.objects.all().order_by("id"),
        empty_label="---------",
    )
    self_tasks = django_filters.BooleanFilter(
        label="Только свои задачи",
        method="filter_self_tasks",
        widget=forms.Select(
            choices=(
                ("", "---------"),
                ("true", "Да"),
                ("false", "Нет"),
            )
        ),
    )

    class Meta:
        model = Task
        fields = ("status", "executor", "labels", "self_tasks")

    def filter_self_tasks(self, queryset, name, value):
        if not value:
            return queryset

        user = getattr(self.request, "user", None)
        if user is None or not user.is_authenticated:
            return queryset.none()

        return queryset.filter(author=user)
