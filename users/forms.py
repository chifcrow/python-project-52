# users/forms.py

from django import forms
from django.contrib.auth import get_user_model


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "username")
