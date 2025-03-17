from ..models import Task, TaskStatus


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
