from typing import Dict, List

from app.models.employee import Employee
from app.models.task import Task

from app.engine.workload import calculate_workload
from app.engine.dependency import find_blocked_tasks


def detect_roadblocks(
    employees: List[Employee],
    tasks: List[Task],
) -> List[Dict]:

    roadblocks = []

    workloads = {
        employee.id: calculate_workload(
            employee,
            tasks
        )
        for employee in employees
    }

    blocked_tasks = find_blocked_tasks(tasks)

    for blocked in blocked_tasks:

        task = next(
            (
                task
                for task in tasks
                if task.id == blocked["task_id"]
            ),
            None
        )

        if task is None:
            continue

        employee = next(
            (
                employee
                for employee in employees
                if employee.id == task.assigned_to
            ),
            None
        )

        workload = None

        if employee:
            workload = workloads[employee.id]

        severity = "medium"

        if workload:
            if workload["workload_percentage"] >= 100:
                severity = "high"

            if (
                workload["workload_percentage"] >= 120
                and task.priority <= 2
            ):
                severity = "critical"

        roadblocks.append({
            "task_id": task.id,
            "task_title": task.title,
            "employee": (
                employee.name
                if employee
                else "Unassigned"
            ),
            "workload": (
                workload["workload_percentage"]
                if workload
                else None
            ),
            "blocked_by": blocked["blocked_by"],
            "severity": severity,
        })

    return roadblocks
