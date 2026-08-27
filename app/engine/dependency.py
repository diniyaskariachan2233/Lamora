from typing import Dict, List

from app.models.task import Task


def find_blocked_tasks(tasks: List[Task]) -> List[Dict]:

    task_map = {
        task.id: task
        for task in tasks
    }

    blocked_tasks = []

    for task in tasks:

        if not task.dependencies:
            continue

        blocking_dependencies = []

        for dependency_id in task.dependencies:

            dependency = task_map.get(dependency_id)

            if dependency is None:
                continue

            if dependency.status != "completed":
                blocking_dependencies.append(
                    dependency.id
                )

        if blocking_dependencies:

            blocked_tasks.append({
                "task_id": task.id,
                "task_title": task.title,
                "blocked_by": blocking_dependencies,
            })

    return blocked_tasks
