from dataclasses import dataclass
from typing import List


@dataclass
class Department:
    id: int
    name: str
    employee_ids: List[int]
    project_ids: List[int]
