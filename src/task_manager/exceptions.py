class TaskManagerError(Exception):
    """Base exception for all task-manager errors."""


class TaskNotFoundError(TaskManagerError):
    def __init__(self, task_id: str):
        super().__init__(f"Task with id '{task_id}' not found.")
        self.task_id = task_id