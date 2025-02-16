from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Task:
    id: int
    description: str
    status: str
    created_at: datetime = datetime.now()
    updated_at: datetime = None

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
