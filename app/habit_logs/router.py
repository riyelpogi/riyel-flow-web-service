from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.habit_logs import service
from app.habit_logs.schemas import CreateHabitLogSchema, HabitLogsResponse

router = APIRouter()


@router.get('/habit-logs', response_model=HabitLogsResponse)
def fetch_habit_logs(
    user_id: int = Query(gt=0),
    habit_id: int | None = Query(default=None, gt=0),
    db: Session = Depends(get_db),
):
    return service.fetch_habit_logs(db=db, user_id=user_id, habit_id=habit_id)
 

@router.post('/habit-logs')
def post_habit_log(payload: CreateHabitLogSchema, db: Session = Depends(get_db)):
    return service.post_habit_log(db=db, payload=payload)
