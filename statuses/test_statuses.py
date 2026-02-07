# statuses/test_statuses.py

import pytest
from django.urls import reverse
from statuses.models import Status


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

    body = response.content.decode()
    assert "Статус успешно создан" in body


@pytest.mark.django_db
def test_status_update(client, user):
    client.force_login(user)

    status = Status.objects.create(name="In progress")
    url = reverse("statuses:update", kwargs={"pk": status.pk})

    response = client.post(url, data={"name": "Done"}, follow=True)

    assert response.status_code == 200
    status.refresh_from_db()
    assert status.name == "Done"

    body = response.content.decode()
    assert "Статус успешно изменен" in body


@pytest.mark.django_db
def test_status_delete(client, user):
    client.force_login(user)

    status = Status.objects.create(name="To delete")
    url = reverse("statuses:delete", kwargs={"pk": status.pk})

    response = client.post(url, follow=True)

    assert response.status_code == 200
    assert not Status.objects.filter(pk=status.pk).exists()

    body = response.content.decode()
    assert "Статус успешно удален" in body


@pytest.mark.django_db
def test_status_delete_protected_error(client, user, monkeypatch):
    client.force_login(user)

    status = Status.objects.create(name="Protected")
    url = reverse("statuses:delete", kwargs={"pk": status.pk})

    from django.db.models.deletion import ProtectedError

    def raise_protected(*args, **kwargs):
        raise ProtectedError("protected", protected_objects=[])

    monkeypatch.setattr(Status, "delete", raise_protected)

    response = client.post(url, follow=True)

    assert response.status_code == 200
    assert Status.objects.filter(pk=status.pk).exists()
    assert "Невозможно удалить статус" in response.content.decode()
