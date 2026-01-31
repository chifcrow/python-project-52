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
        widget=forms.TextInput(
            attrs={"placeholder": "Имя пользователя"}
        ),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Пароль"}
        ),
    )


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        label="Имя",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Имя"}),
    )
    last_name = forms.CharField(
        label="Фамилия",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Фамилия"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        username_field = self.fields["username"]
        username_field.label = "Имя пользователя"
        username_field.help_text = (
            "Обязательное поле. Не более 150 символов. "
            "Только буквы, цифры и символы @/./+/-/_."
        )
        username_field.widget.attrs["placeholder"] = "Имя пользователя"

        password1_field = self.fields["password1"]
        password1_field.label = "Пароль"
        password1_field.help_text = (
            "Ваш пароль должен содержать как минимум 3 символа."
        )
        password1_field.widget.attrs["placeholder"] = "Пароль"

        password2_field = self.fields["password2"]
        password2_field.label = "Подтверждение пароля"
        password2_field.help_text = (
            "Для подтверждения введите, пожалуйста, пароль ещё раз."
        )
        password2_field.widget.attrs["placeholder"] = "Подтверждение пароля"
