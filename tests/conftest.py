#anything defined here is automatically available to all test files
import pytest

from task_manager.service import TaskService
from task_manager.storage import TaskStorage


@pytest.fixture
def storage(tmp_path):
    return TaskStorage(path=tmp_path / "tasks.json")


@pytest.fixture
def service(storage):
    return TaskService(storage=storage)