import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.tasks.models.task import Task
from app.tasks.schemas.create_task_schema import CreateTaskSchema
from app.tasks.schemas.update_task_status_schema import UpdateTaskStatusSchema 
from app.user.models.user import User

logger = logging.getLogger(__name__)


def update_task_status(db: Session, task_id: int, payload: UpdateTaskStatusSchema):
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task is None:
            raise HTTPException(status_code=404, detail='Task not found')

        task.status = payload.status
        db.commit()
        return {'success': True, 'id': task_id, 'status': payload.status}
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        logger.exception('Failed to update task status')
        raise HTTPException(status_code=500, detail='Failed to update task status')


def post_task(db: Session, payload: CreateTaskSchema):
    try:
        user = db.query(User.id).filter(User.id == payload.user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail='User not found')

        task = Task(**payload.model_dump())
        db.add(task)
        db.flush()
        task_id = task.id
        db.commit()
        return {'success': True, 'id': task_id}
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        logger.exception('Failed to create task')
        raise HTTPException(status_code=500, detail='Failed to create task')


def fetch_tasks(db: Session, user_id: int):
    try:
        tasks = (
            db.query(Task)
            .filter(Task.user_id == user_id)
            .order_by(Task.id.desc())
            .all()
        )
        return {'success': True, 'tasks': tasks}
    except Exception:
        logger.exception('Failed to fetch tasks')
        raise HTTPException(status_code=500, detail='Failed to fetch tasks')
