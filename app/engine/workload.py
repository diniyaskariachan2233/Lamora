from typing import Dict, List

from app.models.employee import Employee
from app.models.task import Task


def calculate_workload(
    employee: Employee,
    tasks: List[Task],
) -> Dict:

    assigned_tasks = [
        task
        for task in tasks
        if task.assigned_to == employee.id
        and task.status not in ["completed", "cancelled"]
    ]

    total_hours = sum(
        task.estimated_hours
        for task in assigned_tasks
    )

    capacity = employee.weekly_capacity

    workload_percentage = (
        total_hours / capacity
    ) * 100 if capacity > 0 else 0

    if workload_percentage >= 100:
        status = "overloaded"
    elif workload_percentage >= 80:
        status = "high"
    elif workload_percentage >= 50:
        status = "normal"
    else:
        status = "low"

    return {
        "employee_id": employee.id,
        "employee_name": employee.name,
        "assigned_hours": total_hours,
        "capacity": capacity,
        "workload_percentage": round(workload_percentage, 2),
        "status": status,
        "task_count": len(assigned_tasks),
    }
