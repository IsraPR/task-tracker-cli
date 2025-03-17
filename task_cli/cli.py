import argparse
import os
import json
from .commands import (
    create_task,
    update_task,
    list_tasks,
    mark_as_done,
    mark_as_in_progress,
    delete_task,
)
from .models import TaskStatus

FILE_NAME = "data/tasks.json"
HASHED_IDS = "data/tasks_hashed.json"
PROG = "task-cli"


def main():
    task_cli = argparse.ArgumentParser(
        prog=PROG,
        description="Manage to-do tasks",
        epilog="Happy learning experience",
    )
    subparsers = task_cli.add_subparsers(
        title="subcommands", help="Tasks options"
    )

    # Create task subcommand
    create_task_parser = subparsers.add_parser("add", help="Create a task")
    create_task_parser.add_argument(dest="description", type=str)
    create_task_parser.set_defaults(func=create_task.create_task)

    # Update task subcommand
    update_task_parser = subparsers.add_parser("update", help="Update a task")
    update_task_parser.add_argument(dest="id", type=int)
    update_task_parser.add_argument(dest="description", type=str)
    update_task_parser.set_defaults(func=update_task.update_task)

    # List task subcommand
    list_tasks_parser = subparsers.add_parser("list", help="List all task")
    list_tasks_parser.add_argument(
        dest="status",
        nargs="?",
        choices=TaskStatus,
        type=str,
        default=None,
    )
    list_tasks_parser.set_defaults(func=list_tasks.list_tasks)

    # Mark task as done
    mark_as_done_task_parser = subparsers.add_parser(
        "mark-done", help="Mark a task as done"
    )
    mark_as_done_task_parser.add_argument(dest="id", type=int)
    mark_as_done_task_parser.set_defaults(func=mark_as_done.mark_as_done)

    # Mark as in progress
    mark_as_progress_task_parser = subparsers.add_parser(
        "mark-in-progress", help="Mark a task as in progress"
    )
    mark_as_progress_task_parser.add_argument(dest="id", type=int)
    mark_as_progress_task_parser.set_defaults(
        func=mark_as_in_progress.mark_as_in_progress
    )

    # Delete task
    delete_task_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_task_parser.add_argument(dest="id", type=int)
    delete_task_parser.set_defaults(func=delete_task.delete_task)

    def _get_data_from_args(args):
        data = {}
        for item in args:
            data[item[0]] = item[1]
        return data

    args = task_cli.parse_args()
    if not os.path.exists(FILE_NAME) and not os.path.exists(HASHED_IDS):
        with open(FILE_NAME, "w") as f:
            json.dump({}, f)  # Initialize with an empty json object
        with open(HASHED_IDS, "w") as f:
            json.dump({}, f)  # Initialize with an empty json object
    data = _get_data_from_args(args._get_kwargs()[:-1])
    args.func(**data)


if __name__ == "__main__":
    main()
