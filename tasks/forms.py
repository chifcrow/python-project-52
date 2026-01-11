# tasks/forms.py

from django import forms
from tasks.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("name", "description", "status", "executor", "labels")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["status"].queryset = self.fields[
            "status"].queryset.order_by("id")
        self.fields["executor"].queryset = self.fields[
            "executor"].queryset.order_by(
            "id"
        )
        self.fields["labels"].queryset = self.fields[
            "labels"].queryset.order_by("id")
