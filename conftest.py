import pytest
from django.contrib.auth import get_user_model


@pytest.fixture(name="user")
def _user(db):
    user_model = get_user_model()
    return user_model.objects.create_user(
        username="tester",
        password="password",
    )


@pytest.fixture(name="other_user")
def _other_user(db):
    user_model = get_user_model()
    return user_model.objects.create_user(
        username="other",
        password="password",
    )
