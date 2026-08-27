from typing import Dict, List

from app.models.employee import Employee
from app.models.task import Task

from app.engine.workload import calculate_workload


def recommend_employee(
    task: Task,
    employees: List[Employee],
    all_tasks: List[Task],
) -> Dict:

    candidates = []

    for employee in employees:

        if employee.id == task.assigned_to:
            continue

        workload = calculate_workload(
            employee,
            all_tasks
        )

        if workload["workload_percentage"] >= 100:
            continue

        matching_skills = set(
            task.required_skills
        ).intersection(
            set(employee.skills)
        )

        skill_score = len(matching_skills)

        if skill_score == 0:
            continue

        candidates.append({
            "employee": employee,
            "workload": workload,
            "skill_score": skill_score,
        })

    if not candidates:
        return {
            "recommended": False,
            "message": "No suitable employee found."
        }

    candidates.sort(
        key=lambda candidate: (
            -candidate["skill_score"],
            candidate["workload"]["workload_percentage"]
        )
    )

    best = candidates[0]

    return {
        "recommended": True,
        "employee_id": best["employee"].id,
        "employee_name": best["employee"].name,
        "current_workload": best["workload"][
            "workload_percentage"
        ],
        "matching_skills": best["skill_score"],
        "reason": (
            "Employee has matching skills "
            "and available capacity."
        ),
    }
