# users/test_users.py

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse


@pytest.mark.django_db
def test_user_registration_redirects_to_login(client):
    """
    C (Create): Registration creates a user and redirects to /login/.
    """
    url = reverse("users:create")
    payload = {
        "username": "newuser",
        "password1": "StrongPassword123!",
        "password2": "StrongPassword123!",
    }

    response = client.post(url, data=payload)

    assert response.status_code == 302
    assert response.url == reverse("login")

    User = get_user_model()
    assert User.objects.filter(username="newuser").exists()


@pytest.mark.django_db
def test_user_update_own_profile(client):
    """
    U (Update): A user can update their own profile
    and is redirected to /users/.
    """
    User = get_user_model()
    user = User.objects.create_user(
        username="john",
        password="StrongPassword123!",
        first_name="John",
        last_name="Doe",
    )
    client.force_login(user)

    url = reverse("users:update", kwargs={"pk": user.pk})
    payload = {
        "username": "john_updated",
        "first_name": "Johnny",
        "last_name": "Doe",
    }
    response = client.post(url, data=payload)

    assert response.status_code == 302
    assert response.url == reverse("users:list")

    user.refresh_from_db()
    assert user.username == "john_updated"
    assert user.first_name == "Johnny"


@pytest.mark.django_db
def test_user_update_other_profile_is_forbidden(client):
    """
    U (Update): A user cannot update another user's profile.
    """
    User = get_user_model()
    user1 = User.objects.create_user(
        username="user1",
        password="StrongPassword123!",
    )
    user2 = User.objects.create_user(
        username="user2",
        password="StrongPassword123!",
    )
    client.force_login(user1)

    url = reverse("users:update", kwargs={"pk": user2.pk})
    payload = {
        "username": "hacked",
        "first_name": "Hacker",
        "last_name": "Man",
    }
    response = client.post(url, data=payload)

    assert response.status_code in {302, 403}

    user2.refresh_from_db()
    assert user2.username == "user2"


@pytest.mark.django_db
def test_user_delete_own_profile(client):
    """
    D (Delete): A user can delete their own profile
    and is redirected to /users/.
    """
    User = get_user_model()
    user = User.objects.create_user(
        username="to_delete",
        password="StrongPassword123!",
    )
    client.force_login(user)

    url = reverse("users:delete", kwargs={"pk": user.pk})
    response = client.post(url)

    assert response.status_code == 302
    assert response.url == reverse("users:list")
    assert not User.objects.filter(pk=user.pk).exists()


@pytest.mark.django_db
def test_user_delete_other_profile_is_forbidden(client):
    """
    D (Delete): A user cannot delete another user's profile.
    """
    User = get_user_model()
    user1 = User.objects.create_user(
        username="user1",
        password="StrongPassword123!",
    )
    user2 = User.objects.create_user(
        username="user2",
        password="StrongPassword123!",
    )
    client.force_login(user1)

    url = reverse("users:delete", kwargs={"pk": user2.pk})
    response = client.post(url)

    assert response.status_code in {302, 403}
    assert User.objects.filter(pk=user2.pk).exists()
