from ..models import Task


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
