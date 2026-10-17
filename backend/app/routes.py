from fastapi import APIRouter, Depends, Path
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import Task
from app.schemas import TaskCompletedUpdate, TaskCreate, TaskOut
from app.task_rules import TaskRuleError, check_stored_task, validate_title

router = APIRouter()

class ApiError(Exception):
    def __init__(self, status: int, code: str):
        self.status, self.code = status, code

def check_id(task_id: int) -> int:
    if task_id < 1 or task_id > 2147483647:
        raise ApiError(422, "id_invalid")
    return task_id

def find_task(task_id: int, session: Session) -> Task:
    task_id = check_id(task_id)
    task = session.get(Task, task_id)
    if task is None:
        raise ApiError(404, "task_not_found")
    return task

@router.get("/tasks", response_model=list[TaskOut])
def list_tasks(session: Session = Depends(get_session)):
    tasks = session.scalars(select(Task).order_by(Task.id)).all()
    for task in tasks:
        check_stored_task(task.id, task.title, task.completed)
    return tasks

@router.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(body: TaskCreate, session: Session = Depends(get_session)):
    try:
        title = validate_title(body.title)
    except TaskRuleError as exc:
        raise ApiError(422, exc.code) from exc
    task = Task(title=title, completed=False)
    session.add(task); session.commit(); session.refresh(task)
    return task

@router.patch("/tasks/{task_id}", response_model=TaskOut)
def update_task(body: TaskCompletedUpdate, task_id: int = Path(...), session: Session = Depends(get_session)):
    task = find_task(task_id, session)
    task.completed = body.completed
    session.commit(); session.refresh(task)
    return task

@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int = Path(...), session: Session = Depends(get_session)):
    task = find_task(task_id, session)
    session.delete(task); session.commit()
