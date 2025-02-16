import argparse
import json
import os
from model import Task

# from datetime import datetime
FILE_NAME = "data/tasks.json"
PROG = "task-cli"


def create_task(description: str):
    with open(FILE_NAME, mode="r+") as f:
        try:
            tasks = json.load(f)
        except Exception as e:
            print("Error: ", e)
            tasks = {}

        tasks_length = len(tasks)
        task_id = tasks_length + 1
        task = Task(task_id, description, "todo")
        # TODO: Add validation for same description
        tasks[task_id] = task.as_dict()
        f.seek(0)
        json.dump(tasks, f, indent=4)
        f.truncate()
        print("Task added: ", task)


def update_task():
    pass


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


if __name__ == "__main__":
    args = task_cli.parse_args()
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w") as f:
            json.dump({}, f)  # Initialize with an empty json object
    print(args.func(args.description))
