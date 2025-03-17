from ..models import Task
from ..utils import already_exist


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
