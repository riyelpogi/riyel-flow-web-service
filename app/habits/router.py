from app.habits.schemas.habit_response import HabitsResponse
from app.habits.schemas.habit_schema import CreateHabitSchema
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.habits import service
from app.core.db import get_db

router = APIRouter()

@router.post('/habits')
def post_habit(payload: CreateHabitSchema,db: Session = Depends(get_db)):
    
    res = service.post_habit(db=db, payload=payload)
    
    return res

@router.get('/habits', response_model=HabitsResponse)
def fetch_habits(user_id: int,db: Session = Depends(get_db)):
    
    res = service.fetch_habits(db=db, user_id=user_id)
    
    return res
