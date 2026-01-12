# tasks/test_task_filters.py

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
        username="author1",
        password="StrongPassword123!",
    )


@pytest.fixture()
def other_user(db):
    User = get_user_model()
    return User.objects.create_user(
        username="author2",
        password="StrongPassword123!",
    )


@pytest.fixture()
def executor(db):
    User = get_user_model()
    return User.objects.create_user(
        username="executor",
        password="StrongPassword123!",
    )


@pytest.fixture()
def status_new(db):
    return Status.objects.create(name="New")


@pytest.fixture()
def status_done(db):
    return Status.objects.create(name="Done")


@pytest.fixture()
def label_bug(db):
    return Label.objects.create(name="bug")


@pytest.fixture()
def label_feature(db):
    return Label.objects.create(name="feature")


@pytest.fixture()
def tasks_dataset(
    user,
    other_user,
    executor,
    status_new,
    status_done,
    label_bug,
    label_feature,
):
    t1 = Task.objects.create(
        name="Task A",
        description="",
        status=status_new,
        author=user,
        executor=executor,
    )
    t1.labels.add(label_bug)

    t2 = Task.objects.create(
        name="Task B",
        description="",
        status=status_done,
        author=other_user,
        executor=executor,
    )
    t2.labels.add(label_feature)

    t3 = Task.objects.create(
        name="Task C",
        description="",
        status=status_new,
        author=user,
        executor=None,
    )
    t3.labels.add(label_bug, label_feature)

    return t1, t2, t3


@pytest.mark.django_db
def test_filter_by_status(
    client, user,
    tasks_dataset,
    status_new,
    status_done
):
    client.force_login(user)

    url = reverse("tasks:list")
    response = client.get(url, data={"status": status_new.pk})

    body = response.content.decode()
    assert "Task A" in body
    assert "Task C" in body
    assert "Task B" not in body

    response = client.get(url, data={"status": status_done.pk})
    body = response.content.decode()
    assert "Task B" in body
    assert "Task A" not in body
    assert "Task C" not in body


@pytest.mark.django_db
def test_filter_by_executor(client, user, tasks_dataset, executor):
    client.force_login(user)

    url = reverse("tasks:list")
    response = client.get(url, data={"executor": executor.pk})

    body = response.content.decode()
    assert "Task A" in body
    assert "Task B" in body
    assert "Task C" not in body


@pytest.mark.django_db
def test_filter_by_label(
    client,
    user,
    tasks_dataset,
    label_bug,
    label_feature
):
    client.force_login(user)

    url = reverse("tasks:list")
    response = client.get(url, data={"labels": label_bug.pk})

    body = response.content.decode()
    assert "Task A" in body
    assert "Task C" in body
    assert "Task B" not in body

    response = client.get(url, data={"labels": label_feature.pk})
    body = response.content.decode()
    assert "Task B" in body
    assert "Task C" in body
    assert "Task A" not in body


@pytest.mark.django_db
def test_filter_self_tasks(client, user, tasks_dataset):
    client.force_login(user)

    url = reverse("tasks:list")
    response = client.get(url, data={"self_tasks": "true"})

    body = response.content.decode()
    assert "Task A" in body
    assert "Task C" in body
    assert "Task B" not in body


@pytest.mark.django_db
def test_filter_combined(client, user, tasks_dataset, status_new, label_bug):
    client.force_login(user)

    url = reverse("tasks:list")
    response = client.get(
        url,
        data={
            "status": status_new.pk,
            "labels": label_bug.pk,
            "self_tasks": "true",
        },
    )

    body = response.content.decode()
    assert "Task A" in body
    assert "Task C" in body
    assert "Task B" not in body
