from dataclasses import dataclass, field
from typing import List


@dataclass
class Employee:
    id: int
    name: str
    department: str
    role: str
    skills: List[str]
    weekly_capacity: float = 40.0

    assigned_task_ids: List[int] = field(default_factory=list)
