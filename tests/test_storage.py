import pytest

from task_manager.exceptions import TaskNotFoundError
from task_manager.models import Task, TaskStatus


def test_add_and_get(storage):
    task = storage.add(Task(title="Buy milk"))

    fetched = storage.get(task.id)

    assert fetched.id == task.id
    assert fetched.title == "Buy milk"
    assert fetched.status == TaskStatus.TODO

#compares between the object created and the object fetched from storage

def test_list_all_returns_every_task(storage):
    storage.add(Task(title="Task one"))
    storage.add(Task(title="Task two"))

    tasks = storage.list_all()

    assert len(tasks) == 2


def test_get_missing_task_raises(storage):
    with pytest.raises(TaskNotFoundError):
        storage.get("does-not-exist")


def test_update_changes_fields(storage):
    task = storage.add(Task(title="Original title"))

    updated = storage.update(task.id, title="New title", status=TaskStatus.DONE.value)

    assert updated.title == "New title"
    assert updated.status == TaskStatus.DONE


def test_update_missing_task_raises(storage):
    with pytest.raises(TaskNotFoundError):
        storage.update("does-not-exist", title="Whatever")


def test_delete_removes_task(storage):
    task = storage.add(Task(title="Temporary"))

    storage.delete(task.id)

    assert storage.list_all() == []


def test_delete_missing_task_raises(storage):
    with pytest.raises(TaskNotFoundError):
        storage.delete("does-not-exist")