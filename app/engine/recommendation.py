from typing import Dict, List, Any
from app.models.employee import Employee
from app.models.task import Task
from app.engine.workload import calculate_workload


def score_candidate(
    task: Task,
    employee: Employee,
    workload: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Calculates a multi-factor suitability score (0-100) for a given employee and task.
    """
    reasons: List[str] = []
    
    # 1. Skill Match Score (Max 40 points)
    required_skills = set(task.required_skills)
    employee_skills = set(employee.skills)
    
    if not required_skills:
        skill_score = 40.0
        reasons.append("Task has no specific skill requirements (40/40)")
    else:
        matched_skills = required_skills.intersection(employee_skills)
        match_ratio = len(matched_skills) / len(required_skills)
        skill_score = match_ratio * 40.0
        reasons.append(
            f"Skill match: {len(matched_skills)}/{len(required_skills)} required skills ({round(skill_score, 1)}/40)"
        )

    # 2. Capacity Score (Max 30 points)
    # Remaining capacity percentage before reaching 100%
    available_capacity_pct = max(0.0, 100.0 - workload["workload_percentage"])
    capacity_score = (available_capacity_pct / 100.0) * 30.0
    reasons.append(
        f"Capacity fit: {round(workload['workload_percentage'], 1)}% currently utilized ({round(capacity_score, 1)}/30)"
    )

    # 3. Department Alignment (Max 15 points)
    if employee.department.lower() == task.department.lower():
        department_score = 15.0
        reasons.append("Department match (+15)")
    else:
        department_score = 0.0
        reasons.append("Cross-department match (+0)")

    # 4. Priority & Impact Fit (Max 15 points)
    # High priority tasks (1 or 2) benefit from employees with high available capacity (>50% free)
    if task.priority <= 2:
        if available_capacity_pct >= 50.0:
            priority_score = 15.0
            reasons.append("High priority task assigned to high-capacity candidate (+15)")
        else:
            priority_score = 7.5
            reasons.append("High priority task assigned to moderate-capacity candidate (+7.5)")
    else:
        priority_score = 10.0
        reasons.append("Standard priority task alignment (+10)")

    total_score = round(skill_score + capacity_score + department_score + priority_score, 1)

    return {
        "employee_id": employee.id,
        "employee_name": employee.name,
        "total_score": total_score,
        "breakdown": {
            "skill_score": round(skill_score, 1),
            "capacity_score": round(capacity_score, 1),
            "department_score": round(department_score, 1),
            "priority_score": round(priority_score, 1),
        },
        "reasons": reasons,
        "current_workload_pct": workload["workload_percentage"],
    }


def recommend_employee(
    task: Task,
    employees: List[Employee],
    all_tasks: List[Task],
) -> Dict[str, Any]:
    """
    Evaluates all employees and recommends the candidate with the highest intelligence score.
    """
    candidates = []

    for employee in employees:
        # Skip current assignee
        if employee.id == task.assigned_to:
            continue

        workload = calculate_workload(employee, all_tasks)

        # Skip fully overloaded employees
        if workload["workload_percentage"] >= 100.0:
            continue

        # Skip employees with zero skill overlap if skills are specified
        if task.required_skills:
            has_skill_overlap = any(s in employee.skills for s in task.required_skills)
            if not has_skill_overlap:
                continue

        candidate_eval = score_candidate(task, employee, workload)
        candidates.append(candidate_eval)

    if not candidates:
        return {
            "recommended": False,
            "message": "No suitable candidate found with matching skills and available capacity.",
        }

    # Sort candidates by total score descending, breaking ties with lowest current workload
    candidates.sort(
        key=lambda c: (-c["total_score"], c["current_workload_pct"])
    )

    best = candidates[0]

    return {
        "recommended": True,
        "task_id": task.id,
        "task_title": task.title,
        "recommended_employee_id": best["employee_id"],
        "recommended_employee_name": best["employee_name"],
        "match_score": best["total_score"],
        "score_breakdown": best["breakdown"],
        "reasoning": best["reasons"],
        "all_candidates_evaluated": len(candidates),
    }