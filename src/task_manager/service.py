import logging

from task_manager.models import Task, TaskPriority, TaskStatus
from task_manager.storage import TaskStorage

logger = logging.getLogger(__name__)


class TaskService:
    def __init__(self, storage: TaskStorage | None = None):
        self.storage = storage or TaskStorage()

    def create_task(
        self,
        title: str,
        description: str = "",
        priority: TaskPriority = TaskPriority.MEDIUM,
    ) -> Task:
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty.")

        task = Task(
            title=title.strip(),
            description=description.strip(),
            priority=priority,#not string--> cant strip
        )
        return self.storage.add(task)

    def complete_task(self, task_id: str) -> Task:
        return self.storage.update(task_id, status=TaskStatus.DONE.value)

    def list_tasks(self, status: TaskStatus | None = None) -> list[Task]:
        tasks = self.storage.list_all()

        if status is None:
            return tasks

        return [task for task in tasks if task.status == status]

    def remove_task(self, task_id: str) -> None:
        self.storage.delete(task_id)