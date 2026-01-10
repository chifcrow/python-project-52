# statuses/test_statuses.py

import pytest
from django.contrib.auth import get_user_model
from django.db.models.deletion import ProtectedError
from django.urls import reverse

from statuses.models import Status


@pytest.fixture()
def user(db):
    User = get_user_model()
    return User.objects.create_user(
        username="tester",
        password="StrongPassword123!",
    )


@pytest.mark.django_db
def test_statuses_list_requires_login(client):
    url = reverse("statuses:list")
    response = client.get(url)

    assert response.status_code == 302
    assert response.url.startswith(reverse("login"))


@pytest.mark.django_db
def test_status_create(client, user):
    client.force_login(user)

    url = reverse("statuses:create")
    response = client.post(url, data={"name": "New"}, follow=True)

    assert response.status_code == 200
    assert Status.objects.filter(name="New").exists()
    assert "Status created successfully." in response.content.decode()


@pytest.mark.django_db
def test_status_update(client, user):
    client.force_login(user)

    status = Status.objects.create(name="In progress")
    url = reverse("statuses:update", kwargs={"pk": status.pk})

    response = client.post(url, data={"name": "Done"}, follow=True)

    assert response.status_code == 200
    status.refresh_from_db()
    assert status.name == "Done"
    assert "Status updated successfully." in response.content.decode()


@pytest.mark.django_db
def test_status_delete(client, user):
    client.force_login(user)

    status = Status.objects.create(name="To delete")
    url = reverse("statuses:delete", kwargs={"pk": status.pk})

    response = client.post(url, follow=True)

    assert response.status_code == 200
    assert not Status.objects.filter(pk=status.pk).exists()
    assert "Status deleted successfully." in response.content.decode()


@pytest.mark.django_db
def test_status_delete_protected_error(client, user, monkeypatch):
    client.force_login(user)

    status = Status.objects.create(name="Protected")
    url = reverse("statuses:delete", kwargs={"pk": status.pk})

    def raise_protected(*args, **kwargs):
        raise ProtectedError("protected", protected_objects=[])

    monkeypatch.setattr(Status, "delete", raise_protected)

    response = client.post(url, follow=True)

    assert response.status_code == 200
    assert Status.objects.filter(pk=status.pk).exists()
    assert "Cannot delete status because it is in use." in response.content.decode()
