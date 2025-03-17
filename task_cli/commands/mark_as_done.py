from ..models import Task, TaskStatus


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
