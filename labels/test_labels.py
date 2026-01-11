# labels/test_labels.py

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from labels.models import Label
from statuses.models import Status
from tasks.models import Task


@pytest.fixture()
def user(db):
    User = get_user_model()
    return User.objects.create_user(
        username="tester",
        password="StrongPassword123!",
    )


@pytest.fixture()
def status(db):
    return Status.objects.create(name="New")


@pytest.mark.django_db
def test_labels_list_requires_login(client):
    url = reverse("labels:list")
    response = client.get(url)

    assert response.status_code == 302
    assert response.url.startswith(reverse("login"))


@pytest.mark.django_db
def test_label_create(client, user):
    client.force_login(user)

    url = reverse("labels:create")
    response = client.post(url, data={"name": "bug"}, follow=True)

    assert response.status_code == 200
    assert Label.objects.filter(name="bug").exists()
    assert "Label created successfully." in response.content.decode()


@pytest.mark.django_db
def test_label_update(client, user):
    client.force_login(user)

    label = Label.objects.create(name="feature")
    url = reverse("labels:update", kwargs={"pk": label.pk})

    response = client.post(url, data={"name": "enhancement"}, follow=True)

    assert response.status_code == 200
    label.refresh_from_db()
    assert label.name == "enhancement"
    assert "Label updated successfully." in response.content.decode()


@pytest.mark.django_db
def test_label_delete(client, user):
    client.force_login(user)

    label = Label.objects.create(name="to_delete")
    url = reverse("labels:delete", kwargs={"pk": label.pk})

    response = client.post(url, follow=True)

    assert response.status_code == 200
    assert not Label.objects.filter(pk=label.pk).exists()
    assert "Label deleted successfully." in response.content.decode()


@pytest.mark.django_db
def test_label_delete_is_blocked_when_used_by_task(client, user, status):
    client.force_login(user)

    label = Label.objects.create(name="in_use")

    task = Task.objects.create(
        name="Task with label",
        description="",
        status=status,
        author=user,
    )
    task.labels.add(label)

    url = reverse("labels:delete", kwargs={"pk": label.pk})
    response = client.post(url, follow=True)

    assert response.status_code == 200
    assert Label.objects.filter(pk=label.pk).exists()

    body = response.content.decode()
    expected = "Cannot delete label because it is in use."
    assert expected in body
