from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.tasks import service
from app.tasks.schemas.create_task_response import CreateTaskResponse
from app.tasks.schemas.create_task_schema import CreateTaskSchema
from app.tasks.schemas.tasks_response import TasksResponse
from app.tasks.schemas.update_task_status_schema import UpdateTaskStatusSchema
from app.tasks.schemas.update_task_status_response import UpdateTaskStatusResponse

router = APIRouter()


@router.patch('/tasks/{task_id}/status', response_model=UpdateTaskStatusResponse)
def update_task_status(
    payload: UpdateTaskStatusSchema,
    task_id: int = Path(gt=0),
    db: Session = Depends(get_db),
):
    return service.update_task_status(db=db, task_id=task_id, payload=payload)


@router.post('/tasks', response_model=CreateTaskResponse, status_code=201)
def post_task(payload: CreateTaskSchema, db: Session = Depends(get_db)):
    return service.post_task(db=db, payload=payload)


@router.get('/tasks', response_model=TasksResponse)
def fetch_tasks(user_id: int = Query(gt=0), db: Session = Depends(get_db)):
    return service.fetch_tasks(db=db, user_id=user_id)
