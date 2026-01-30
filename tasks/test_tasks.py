# tasks/test_tasks.py

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from statuses.models import Status
from tasks.models import Task


@pytest.fixture()
def user(db):
    User = get_user_model()
    return User.objects.create_user(
        username="author",
        password="StrongPassword123!",
    )


@pytest.fixture()
def other_user(db):
    User = get_user_model()
    return User.objects.create_user(
        username="other",
        password="StrongPassword123!",
    )


@pytest.fixture()
def status(db):
    return Status.objects.create(name="New")


@pytest.mark.django_db
def test_tasks_list_requires_login(client):
    url = reverse("tasks:list")
    response = client.get(url)

    assert response.status_code == 302
    assert response.url.startswith(reverse("login"))


@pytest.mark.django_db
def test_task_create_sets_author(client, user, other_user, status):
    client.force_login(user)

    url = reverse("tasks:create")
    payload = {
        "name": "Test task",
        "description": "Some description",
        "status": status.pk,
        "executor": other_user.pk,
        "labels": [],
    }
    response = client.post(url, data=payload)

    assert response.status_code == 302
    assert response.url == reverse("tasks:list")

    task = Task.objects.get(name="Test task")
    assert task.author_id == user.pk
    assert task.executor_id == other_user.pk
    assert task.status_id == status.pk


@pytest.mark.django_db
def test_task_detail_requires_login(client, user, status):
    task = Task.objects.create(
        name="Detail task",
        description="",
        status=status,
        author=user,
    )

    url = reverse("tasks:detail", kwargs={"pk": task.pk})
    response = client.get(url)

    assert response.status_code == 302
    assert response.url.startswith(reverse("login"))


@pytest.mark.django_db
def test_task_update(client, user, status):
    client.force_login(user)

    task = Task.objects.create(
        name="Old name",
        description="Old",
        status=status,
        author=user,
    )

    url = reverse("tasks:update", kwargs={"pk": task.pk})
    payload = {
        "name": "New name",
        "description": "New",
        "status": status.pk,
        "executor": "",
        "labels": [],
    }
    response = client.post(url, data=payload)

    assert response.status_code == 302
    assert response.url == reverse("tasks:list")

    task.refresh_from_db()
    assert task.name == "New name"
    assert task.description == "New"


@pytest.mark.django_db
def test_task_delete_only_author_can_delete(client, user, other_user, status):
    task = Task.objects.create(
        name="To delete",
        description="",
        status=status,
        author=user,
    )

    url = reverse("tasks:delete", kwargs={"pk": task.pk})

    client.force_login(other_user)
    response = client.post(url, follow=True)

    assert response.status_code == 200
    assert Task.objects.filter(pk=task.pk).exists()

    body = response.content.decode()
    assert "Задачу может удалить только её автор." in body

    client.force_login(user)
    response = client.post(url, follow=True)

    assert response.status_code == 200
    assert not Task.objects.filter(pk=task.pk).exists()

    body = response.content.decode()
    assert "Задача успешно удалена." in body


@pytest.mark.django_db
def test_user_deletion_is_protected_when_authored_tasks_exist(user, status):
    Task.objects.create(
        name="Authored",
        description="",
        status=status,
        author=user,
    )

    with pytest.raises(Exception):
        user.delete()
