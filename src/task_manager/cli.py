import argparse
import logging
import sys

from task_manager.config import settings
from task_manager.exceptions import TaskManagerError
from task_manager.models import Task, TaskPriority, TaskStatus
from task_manager.service import TaskService

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="task-manager",
        description="A simple command-line task manager.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", type=str, help="Task title")
    add_parser.add_argument("-desc", "--description", type=str, default="")
    add_parser.add_argument(
        "-prio", "--priority",
        choices=[p.value for p in TaskPriority],
        default=TaskPriority.MEDIUM.value,
    )

    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument(
        "-stat", "--status",
        choices=[s.value for s in TaskStatus],
        default=None,
    )

    complete_parser = subparsers.add_parser("complete", help="Mark a task as done")
    complete_parser.add_argument("task_id", type=str)

    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", type=str)

    return parser


def format_task(task: Task) -> str:
    return f"[{task.status.value:^11}] {task.id[:8]}  {task.title}  (priority: {task.priority.value})"
# ^11: center alingment
#:8 takes the first 8 characters of the task UUID for display

def main() -> None:
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    parser = build_parser()
    args = parser.parse_args()
    service = TaskService()

    try:
        if args.command == "add":
            task = service.create_task(
                title=args.title,
                description=args.description,
                priority=TaskPriority(args.priority),
            )
            print(f"Created task {task.id[:8]}: {task.title}")

        elif args.command == "list":
            status_filter = TaskStatus(args.status) if args.status else None
            tasks = service.list_tasks(status=status_filter)
            if not tasks:
                print("No tasks found.")
            for task in tasks:
                print(format_task(task))

        elif args.command == "complete":
            task = service.complete_task(args.task_id)
            print(f"Marked task {task.id[:8]} as done.")

        elif args.command == "delete":
            service.remove_task(args.task_id)
            print(f"Deleted task {args.task_id[:8]}.")

    except (ValueError, TaskManagerError) as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()