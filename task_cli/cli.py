import argparse
import json
import os
from model import Task, TaskStatus
from utils import create_md5_id, already_exist, update_hashed
from datetime import datetime

# from datetime import datetime
FILE_NAME = "data/tasks.json"
HASHED_IDS = "data/tasks_hashed.json"
PROG = "task-cli"


def create_task(description: str):
    tasks_length = Task.count()
    task_id = tasks_length + 1
    task_id = Task.create_if_exist(id=task_id)
    task = Task(
        id=task_id,
        description=description,
    )
    if not already_exist(
        hashed_id=task.hash_id,
        task_id=task.id,
        add=True,
    ):
        task.save()
        print("Task added: ", task)
    else:
        print("Task already exist!")


def update_task(id: int, description: str):
    _task = Task.get(task_id=id)
    if _task:
        new_hashed = create_md5_id(description)
        if not already_exist(hashed_id=new_hashed):
            _task.description = description
            update_hashed(
                new_hashed_id=new_hashed,
                old_hashed=_task.hash_id,
                task_id=id,
            )
            _task.hash_id = new_hashed
            _task.updated_at = datetime.now()
            _task.save()
            print(f"Task {id} updated: {_task}")

        else:
            print("Task with same description already exist!")
    else:
        print("Task not found!")


def list_tasks(status: str = None):
    if status:
        tasks = Task.query(status=status)
    else:
        tasks = Task.query()
    if tasks:
        print("ID\tStatus\tDescription")
        for task in tasks:
            print(task)
    else:
        print("No tasks to list")


def mark_as_done(id: int):
    task = Task.get(task_id=id)
    if task:
        if not task.status == TaskStatus.DONE.value:

            task.status = TaskStatus.DONE.value
            task.save()
            print(f"Task mark as done: {task}")
        else:
            print("Task already marked as done")
    else:
        print("Task not found")


def mark_as_in_progress(id: int):
    task = Task.get(task_id=id)
    if task:
        if not task.status == TaskStatus.IN_PROGRESS.value:
            task.status = TaskStatus.IN_PROGRESS.value
            task.save()
            print(f"Task mark as in progress: {task}")
        else:
            print("Task already marked as in progress")
    else:
        print("Task not found")


def delete_task(id: int):
    if Task.get(task_id=id):
        Task.delete(task_id=id)
        print("Task deleted!")
    else:
        print("Task nof found")


task_cli = argparse.ArgumentParser(
    prog=PROG,
    description="Manage to-do tasks",
    epilog="Happy learning experience",
)
subparsers = task_cli.add_subparsers(title="subcommands", help="Tasks options")

# Create task subcommand
create_task_parser = subparsers.add_parser("add", help="Create a task")
create_task_parser.add_argument(dest="description", type=str)
create_task_parser.set_defaults(func=create_task)

# Update task subcommand
update_task_parser = subparsers.add_parser("update", help="Update a task")
update_task_parser.add_argument(dest="id", type=int)
update_task_parser.add_argument(dest="description", type=str)
update_task_parser.set_defaults(func=update_task)

# List task subcommand
list_tasks_parser = subparsers.add_parser("list", help="List all task")
list_tasks_parser.add_argument(
    dest="status",
    nargs="?",
    choices=TaskStatus,
    type=str,
    default=None,
)
list_tasks_parser.set_defaults(func=list_tasks)

# Mark task as done
mark_as_done_task_parser = subparsers.add_parser(
    "mark-done", help="Mark a task as done"
)
mark_as_done_task_parser.add_argument(dest="id", type=int)
mark_as_done_task_parser.set_defaults(func=mark_as_done)

# Mark as in progress
mark_as_progress_task_parser = subparsers.add_parser(
    "mark-in-progress", help="Mark a task as in progress"
)
mark_as_progress_task_parser.add_argument(dest="id", type=int)
mark_as_progress_task_parser.set_defaults(func=mark_as_in_progress)


# Mark as in progress
delete_task_parser = subparsers.add_parser("delete", help="Delete a task")
delete_task_parser.add_argument(dest="id", type=int)
delete_task_parser.set_defaults(func=delete_task)


def _get_data_from_args(args):
    data = {}
    for item in args:
        data[item[0]] = item[1]
    return data


if __name__ == "__main__":
    args = task_cli.parse_args()
    if not os.path.exists(FILE_NAME) and not os.path.exists(HASHED_IDS):
        with open(FILE_NAME, "w") as f:
            json.dump({}, f)  # Initialize with an empty json object
        with open(HASHED_IDS, "w") as f:
            json.dump({}, f)  # Initialize with an empty json object
    data = _get_data_from_args(args._get_kwargs()[:-1])
    args.func(**data)
