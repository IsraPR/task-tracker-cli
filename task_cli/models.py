import json
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from .utils import create_md5_id

FILE_NAME = "data/tasks.json"
HASHED_IDS = "data/tasks_hashed.json"


class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"


@dataclass
class Task:
    id: int = None
    description: str = ""
    status: str = TaskStatus.TODO.value
    created_at: datetime = datetime.now()
    updated_at: datetime = None
    hash_id: str = None

    def __post_init__(self):
        self.hash_id = create_md5_id(self.description)

    def as_dict(self):
        rep_dict = asdict(self)
        if self.created_at:
            rep_dict["created_at"] = self.created_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        if self.updated_at:
            rep_dict["updated_at"] = self.updated_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        return rep_dict

    def __str__(self):
        return f"{self.id}\t{self.status}\t{self.description}"

    @classmethod
    def count(cls):
        with open(FILE_NAME, mode="r+") as f:
            try:
                tasks = json.load(f)
            except Exception as e:
                print("Error: ", e)
                tasks = {}
            return len(tasks)

    @classmethod
    def create_if_exist(csl, id):
        with open(FILE_NAME, mode="r+") as f:
            try:
                tasks = json.load(f)
            except Exception as e:
                print("Error: ", e)
                tasks = {}
        available_id = id
        while tasks.get(f"{available_id}", None):
            available_id += 1
        return available_id

    @classmethod
    def query(cls, status: str = None):
        with open(FILE_NAME, mode="r+") as f:
            try:
                tasks = json.load(f)
            except Exception as e:
                print("Error: ", e)
                tasks = {}
            if status:
                return [
                    cls(**task)
                    for task in tasks.values()
                    if task.get("status") == status
                ]
            else:
                return [cls(**task) for task in tasks.values()]

    @classmethod
    def get(cls, task_id: int):
        with open(FILE_NAME, mode="r+") as f:
            try:
                tasks = json.load(f)
            except Exception as e:
                print("Error: ", e)
                tasks = {}

            if task := tasks.get(f"{task_id}"):
                task["created_at"] = datetime.strptime(
                    task["created_at"], "%Y-%m-%d %H:%M:%S"
                )
                task["updated_at"] = (
                    datetime.strptime(task["updated_at"], "%Y-%m-%d %H:%M:%S")
                    if task["updated_at"]
                    else None
                )
                return cls(**task)
            else:
                return None

    @classmethod
    def delete(cls, task_id: int):
        with open(FILE_NAME, mode="r+") as f:
            try:
                tasks = json.load(f)
            except Exception as e:
                print("Error: ", e)
                tasks = {}

            task = tasks.pop(f"{task_id}")
            f.seek(0, 0)
            json.dump(tasks, f, indent=4)
            f.truncate()
        with open(HASHED_IDS, mode="r+") as f:
            try:
                hash_tasks = json.load(f)
            except Exception as e:
                print("Error: ", e)
                hash_tasks = {}
            hash_tasks.pop(task.get("hash_id"))
            f.seek(0, 0)
            json.dump(hash_tasks, f, indent=4)
            f.truncate()

    def save(self):
        with open(FILE_NAME, mode="r+") as f:
            try:
                tasks = json.load(f)
            except Exception as e:
                print("Error: ", e)
                tasks = {}
            tasks[f"{self.id}"] = self.as_dict()
            f.seek(0, 0)
            json.dump(tasks, f, indent=4)
            f.truncate()
