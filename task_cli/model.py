import json
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from utils import create_md5_id

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
        return f"{self.id}\t{self.description}"

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
    def query(cls):
        with open(FILE_NAME, mode="r+") as f:
            try:
                tasks = json.load(f)
            except Exception as e:
                print("Error: ", e)
                tasks = {}
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

    def save(self):
        with open(FILE_NAME, mode="r+") as f:
            try:
                tasks = json.load(f)
            except Exception as e:
                print("Error: ", e)
                tasks = {}
            tasks[self.id] = self.as_dict()
            f.seek(0)
            json.dump(tasks, f, indent=4)
            f.truncate()
