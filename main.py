from fastapi import FastAPI

from app.data.sample_data import employees, tasks

from app.engine.workload import calculate_workload
from app.engine.roadblock import detect_roadblocks
from app.engine.recommendation import recommend_employee


app = FastAPI(
    title="Operational Intelligence Engine",
    version="0.1.0",
)


@app.get("/")
def home():
    return {
        "message": "Operational Intelligence Engine"
    }


@app.get("/workloads")
def workloads():

    return [
        calculate_workload(
            employee,
            tasks
        )
        for employee in employees
    ]


@app.get("/roadblocks")
def roadblocks():

    return detect_roadblocks(
        employees,
        tasks
    )


@app.get("/recommendation/{task_id}")
def recommendation(task_id: int):

    task = next(
        (
            task
            for task in tasks
            if task.id == task_id
        ),
        None
    )

    if task is None:
        return {
            "error": "Task not found"
        }

    return recommend_employee(
        task,
        employees,
        tasks
    )
