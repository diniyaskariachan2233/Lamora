from app.models.employee import Employee
from app.models.task import Task


employees = [

    Employee(
        id=1,
        name="Alex",
        department="Engineering",
        role="Backend Developer",
        skills=["Python", "FastAPI", "PostgreSQL"],
        weekly_capacity=40,
    ),

    Employee(
        id=2,
        name="Sarah",
        department="Engineering",
        role="Backend Developer",
        skills=["Python", "FastAPI", "PostgreSQL"],
        weekly_capacity=40,
    ),

    Employee(
        id=3,
        name="David",
        department="Operations",
        role="Operations Manager",
        skills=["Operations", "Management"],
        weekly_capacity=40,
    ),
]


tasks = [

    Task(
        id=101,
        title="Payment API",
        assigned_to=1,
        department="Engineering",
        required_skills=["Python", "FastAPI"],
        estimated_hours=20,
        priority=1,
        status="in_progress",
    ),

    Task(
        id=102,
        title="Database Migration",
        assigned_to=1,
        department="Engineering",
        required_skills=["PostgreSQL"],
        estimated_hours=15,
        priority=2,
        status="pending",
        dependencies=[101],
    ),

    Task(
        id=103,
        title="API Testing",
        assigned_to=2,
        department="Engineering",
        required_skills=["Python"],
        estimated_hours=10,
        priority=2,
        status="in_progress",
    ),
]
