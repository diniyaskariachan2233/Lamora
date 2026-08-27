from dataclasses import dataclass
from typing import List


@dataclass
class Project:
    id: int
    name: str
    task_ids: List[int]
    deadline_days: int
    status: str = "active"
