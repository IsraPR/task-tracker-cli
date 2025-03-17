from datetime import datetime
from ..models import Task
from ..utils import create_md5_id, already_exist, update_hashed


def update_task(id: int, description: str):
    task = Task.get(task_id=id)
    if task:
        new_hashed = create_md5_id(description)
        if not already_exist(hashed_id=new_hashed):
            task.description = description
            update_hashed(
                new_hashed_id=new_hashed,
                old_hashed=task.hash_id,
                task_id=id,
            )
            task.hash_id = new_hashed
            task.updated_at = datetime.now()
            task.save()
            print(f"Task {id} updated: {task}")

        else:
            print("Task with same description already exist!")
    else:
        print("Task not found!")
