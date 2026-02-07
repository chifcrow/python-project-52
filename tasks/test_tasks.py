# tasks/test_tasks.py

import pytest
from django.urls import reverse

from statuses.models import Status
from tasks.models import Task


@pytest.fixture(name="status")
def _status(db):
    return Status.objects.create(name="New")


@pytest.mark.django_db
def test_tasks_list_requires_login(client):
    url = reverse("tasks:list")
    response = client.get(url)

    assert response.status_code == 302
    assert response.url.startswith(reverse("login"))


@pytest.mark.django_db
def test_task_create(client, user, status):
    client.force_login(user)

    url = reverse("tasks:create")
    response = client.post(
        url,
        data={
            "name": "Task name",
            "description": "Task description",
            "status": status.pk,
        },
        follow=True,
    )

    assert response.status_code == 200
    assert Task.objects.filter(name="Task name").exists()
    assert "Задача успешно создана" in response.content.decode()


@pytest.mark.django_db
def test_task_update(client, user, status):
    client.force_login(user)

    task = Task.objects.create(
        name="Old name",
        description="",
        status=status,
        author=user,
    )

    url = reverse("tasks:update", kwargs={"pk": task.pk})
    response = client.post(
        url,
        data={
            "name": "New name",
            "description": "Updated",
            "status": status.pk,
        },
        follow=True,
    )

    assert response.status_code == 200
    task.refresh_from_db()
    assert task.name == "New name"
    assert "Задача успешно изменена" in response.content.decode()


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
    assert "Задачу может удалить только ее автор" in response.content.decode()


@pytest.mark.django_db
def test_task_delete_as_author(client, user, status):
    client.force_login(user)

    task = Task.objects.create(
        name="To delete",
        description="",
        status=status,
        author=user,
    )

    url = reverse("tasks:delete", kwargs={"pk": task.pk})
    response = client.post(url, follow=True)

    assert response.status_code == 200
    assert not Task.objects.filter(pk=task.pk).exists()
    assert "Задача успешно удалена" in response.content.decode()
