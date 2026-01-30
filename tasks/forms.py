# tasks/forms.py

from django import forms

from tasks.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("name", "description", "status", "executor", "labels")
        labels = {
            "name": "Название",
            "description": "Описание",
            "status": "Статус",
            "executor": "Исполнитель",
            "labels": "Метки",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        status_qs = self.fields["status"].queryset
        self.fields["status"].queryset = status_qs.order_by("id")

        executor_qs = self.fields["executor"].queryset
        self.fields["executor"].queryset = executor_qs.order_by("id")

        labels_qs = self.fields["labels"].queryset
        self.fields["labels"].queryset = labels_qs.order_by("id")
