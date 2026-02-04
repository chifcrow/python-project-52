# statuses/forms.py

from django import forms

from statuses.models import Status


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ("name",)
        labels = {"name": "Имя"}
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Имя"}),
        }
