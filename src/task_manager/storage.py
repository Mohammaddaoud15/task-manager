import json
import logging
from contextlib import contextmanager
from pathlib import Path

from task_manager.config import settings
from task_manager.exceptions import TaskNotFoundError
from task_manager.models import Task

logger = logging.getLogger(__name__)


class TaskStorage:
    def __init__(self, path: Path | None = None):
        self.path = path or settings.storage_path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]") # create json file if it doesn't exist
 
            

    @contextmanager
    def _load_and_save(self):
        """Load tasks, yield the list for mutation, then persist it back."""
        tasks = self._read_all()
        yield tasks
        self._write_all(tasks)

    def _read_all(self) -> list[dict]:
        return json.loads(self.path.read_text()) #self.path returns .json

    def _write_all(self, tasks: list[dict]) -> None:
        self.path.write_text(json.dumps(tasks, indent=2))#.dumps() converts python object to json string

    def add(self, task: Task) -> Task:
        with self._load_and_save() as tasks:
            tasks.append(task.to_dict())# json cannot deal with task object, so we convert it to dict

        logger.info(f"Added task {task.id}")
        return task

    def get(self, task_id: str) -> Task:
        tasks = self._read_all()

        for task in tasks:
            if task["id"] == task_id:
                return Task.from_dict(task)

        raise TaskNotFoundError(task_id)

    def list_all(self) -> list[Task]:
        return [Task.from_dict(task) for task in self._read_all()]

    def update(self, task_id: str, **changes) -> Task:
        with self._load_and_save() as tasks:
            for task in tasks:
                if task["id"] == task_id:
                    task.update(changes)
                    logger.info(f"Updated task {task_id}")
                    return Task.from_dict(task)

        raise TaskNotFoundError(task_id)

    def delete(self, task_id: str) -> None:
        with self._load_and_save() as tasks:

            for task in tasks:
                if task["id"] == task_id:
                    tasks.remove(task)
                    logger.info(f"Deleted task {task_id}")
                    return

        raise TaskNotFoundError(task_id)
    
