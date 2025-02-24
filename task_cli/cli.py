import argparse
import json
import os
from model import Task
from utils import create_md5_id, already_exist, update_hashed
from datetime import datetime

# from datetime import datetime
FILE_NAME = "data/tasks.json"
HASHED_IDS = "data/tasks_hashed.json"
PROG = "task-cli"


def create_task(task: Task):
    tasks_length = Task.count()
    task_id = tasks_length + 1
    task.id = task_id
    if not already_exist(
        hashed_id=task.hash_id,
        task_id=task.id,
        add=True,
    ):
        task.save()
        print("Task added: ", task)
    else:
        print("Task already exist!")


def update_task(task: Task):
    _task = Task.get(task_id=task.id)
    if _task:
        new_hashed = create_md5_id(task.description)
        if not already_exist(hashed_id=new_hashed):
            _task.description = task.description
            update_hashed(
                new_hashed_id=new_hashed,
                old_hashed=_task.hash_id,
                task_id=task.id,
            )
            _task.hash_id = new_hashed
            _task.updated_at = datetime.now()
            _task.save()
            print(f"Task {task.id} updated: {task}")

        else:
            print("Task with same description already exist!")
    else:
        print("Task not found!")


def list_tasks():
    tasks = Task.query()
    if tasks:
        print("ID\tDescription")
        for task in tasks:
            print(task)
    else:
        print("No tasks to list")


task_cli = argparse.ArgumentParser(
    prog=PROG,
    description="Manage to-do tasks",
    epilog="Happy learning experience",
)
subparsers = task_cli.add_subparsers(title="subcommands", help="Tasks options")

# Create a task subcommand
create_task_parser = subparsers.add_parser("add", help="Create a task")
create_task_parser.add_argument(dest="description", type=str)
create_task_parser.set_defaults(func=create_task)

# Update a task subcommand
create_task_parser = subparsers.add_parser("update", help="Update a task")
create_task_parser.add_argument(dest="id", type=int)
create_task_parser.add_argument(dest="description", type=str)
create_task_parser.set_defaults(func=update_task)


# List task
create_task_parser = subparsers.add_parser("list", help="List all task")
create_task_parser.set_defaults(func=list_tasks)


def _create_task_from_args(args):
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

    if len(args._get_kwargs()) > 1:
        task_data = _create_task_from_args(args._get_kwargs()[:-1])
        task = Task(**task_data)
        args.func(task)
    else:
        args.func()
