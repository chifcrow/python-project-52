# tasks/forms.py

from django import forms

from tasks.models import Task


def display_user_name(user) -> str:
    # Prefer first/last name; fallback to username formatted as title.
    first = (getattr(user, "first_name", "") or "").strip()
    last = (getattr(user, "last_name", "") or "").strip()
    if first or last:
        return f"{first} {last}".strip()

    username = (getattr(user, "username", "") or "").strip()
    if not username:
        return "-"

    return username.replace("-", " ").replace("_", " ").title()


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("name", "description", "status", "executor", "labels")
        labels = {
            "name": "Имя",
            "description": "Описание",
            "status": "Статус",
            "executor": "Исполнитель",
            "labels": "Метки",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Имя"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        status_qs = self.fields["status"].queryset
        self.fields["status"].queryset = status_qs.order_by("id")

        executor_qs = self.fields["executor"].queryset
        self.fields["executor"].queryset = executor_qs.order_by("id")
        self.fields["executor"].label_from_instance = display_user_name

        labels_qs = self.fields["labels"].queryset
        self.fields["labels"].queryset = labels_qs.order_by("id")
