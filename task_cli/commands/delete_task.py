from ..models import Task


def delete_task(id: int):
    if Task.get(task_id=id):
        Task.delete(task_id=id)
        print("Task deleted!")
    else:
        print("Task nof found")
