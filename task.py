from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Task:
    id: int
    title: str
    assigned_to: Optional[int]
    department: str
    required_skills: List[str]

    estimated_hours: float
    priority: int

    status: str = "pending"
    deadline_days: int = 7

    dependencies: List[int] = field(default_factory=list)
