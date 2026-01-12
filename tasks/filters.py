# tasks/filters.py

import django_filters
from django.contrib.auth import get_user_model
from labels.models import Label
from statuses.models import Status
from tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all().order_by("id"),
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=get_user_model().objects.all().order_by("id"),
    )
    labels = django_filters.ModelChoiceFilter(
        field_name="labels",
        queryset=Label.objects.all().order_by("id"),
    )
    self_tasks = django_filters.BooleanFilter(method="filter_self_tasks")

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
