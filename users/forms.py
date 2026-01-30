# users/forms.py

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "username")
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "username": "Имя пользователя",
        }


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={"placeholder": "Имя пользователя"}),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"placeholder": "Пароль"}),
    )


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].label = "Имя пользователя"
        self.fields["username"].help_text = (
            "Обязательное поле. До 150 символов. "
            "Буквы, цифры и символы @/./+/-/_"
        )
        self.fields["username"].widget.attrs["placeholder"] = \
            "Имя пользователя"

        self.fields["password1"].label = "Пароль"
        self.fields["password1"].help_text = (
            "Пароль должен быть достаточно сложным."
        )
        self.fields["password1"].widget.attrs["placeholder"] = "Пароль"

        self.fields["password2"].label = "Подтверждение пароля"
        self.fields["password2"].help_text = (
            "Введите тот же пароль ещё раз для подтверждения."
        )
        self.fields["password2"].widget.attrs["placeholder"] = (
            "Подтверждение пароля"
        )
