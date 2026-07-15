from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4

#name=TODO , value=todo
class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

# no default valus means its required, so title is required, description is optional with default value of empty string
@dataclass
class Task:
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    #default factory is used to generate a new unique id for each task using uuid4, and to set the created_at timestamp to the current time in ISO format
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    #JSON understand iso format
    def to_dict(self) -> dict:
        return {
        "title": self.title,
        "description": self.description,
        "status": self.status.value,
        "priority": self.priority.value,
        "id": self.id,
        "created_at": self.created_at,
        }
    @classmethod #--> allows the method to deal with the class itself 
    def from_dict(cls, data: dict) -> "Task":
        return cls( #cls--> refers to the class itself, so cls(...) creates a new instance of the Task class using the provided data dictionary
        title=data["title"],
        description=data.get("description", ""),
        status=TaskStatus(data["status"]),#enum
        priority=TaskPriority(data["priority"]),#enum
        id=data["id"],
        created_at=data["created_at"],
        )