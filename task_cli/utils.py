import json
import hashlib

HASHED_IDS = "data/tasks_hashed.json"


def create_md5_id(input_str: str) -> str:
    # Encode the input string to bytes, then compute the MD5 hash.
    md5_hash = hashlib.md5(input_str.encode("utf-8"))
    # Return the hexadecimal digest of the hash.
    return md5_hash.hexdigest()


def already_exist(hashed_id: str, task_id: int = None, add=False):
    with open(HASHED_IDS, mode="r+") as f:
        try:
            tasks = json.load(f)
        except Exception as e:
            print("Error: ", e)
            tasks = {}
        if hashed_id in tasks:
            return True
        elif add:
            tasks[hashed_id] = task_id
            f.seek(0)
            json.dump(tasks, f, indent=4)
            f.truncate()


def update_hashed(new_hashed_id: str, old_hashed: str, task_id: int):
    with open(HASHED_IDS, mode="r+") as f:
        try:
            tasks = json.load(f)
        except Exception as e:
            print("Error: ", e)
            tasks = {}
        tasks[new_hashed_id] = task_id
        tasks.pop(old_hashed)
        f.seek(0)
        json.dump(tasks, f, indent=4)
        f.truncate()
