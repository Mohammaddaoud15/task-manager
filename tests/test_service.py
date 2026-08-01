import pytest

from task_manager.exceptions import TaskNotFoundError
from task_manager.models import TaskPriority, TaskStatus
from task_manager.service import TaskService


def test_create_task_success(service):
    task = service.create_task("Write report", priority=TaskPriority.HIGH)

    assert task.title == "Write report"
    assert task.priority == TaskPriority.HIGH
    assert task.status == TaskStatus.TODO

#compares the task's own attributes with the values the test already knows

def test_create_task_strips_whitespace(service):
    task = service.create_task("  Buy milk  ")

    assert task.title == "Buy milk"


@pytest.mark.parametrize("bad_title", ["", "   ", None])
def test_create_task_rejects_invalid_title(service, bad_title):
    with pytest.raises(ValueError):
        service.create_task(bad_title)


def test_complete_task_sets_status_done(service):
    task = service.create_task("Finish this")

    completed = service.complete_task(task.id)

    assert completed.status == TaskStatus.DONE


def test_list_tasks_filters_by_status(service):
    service.create_task("Task A")
    done_task = service.create_task("Task B")
    service.complete_task(done_task.id)

    todo_tasks = service.list_tasks(status=TaskStatus.TODO)
    done_tasks = service.list_tasks(status=TaskStatus.DONE)

    assert len(todo_tasks) == 1
    assert len(done_tasks) == 1
    assert todo_tasks[0].title == "Task A"
    assert done_tasks[0].title == "Task B"


def test_remove_task_deletes_it(service):
    task = service.create_task("Temporary")

    service.remove_task(task.id)

    with pytest.raises(TaskNotFoundError):
        service.storage.get(task.id)


def test_create_task_calls_storage_add(mocker):
    

    fake_storage = mocker.Mock()
    fake_storage.add.side_effect = lambda task: task

    svc = TaskService(storage=fake_storage)
    svc.create_task("Whatever")

    fake_storage.add.assert_called_once()