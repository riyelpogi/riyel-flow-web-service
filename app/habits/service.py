

from app.utils.date_periods import get_periods
from fastapi import HTTPException

from fastapi.responses import JSONResponse
from sqlalchemy import exists
from sqlalchemy.orm import Session
from starlette import status

from app.habit_logs.models.habit_log import HabitLog
from app.habits.models.habit import Habit
from app.habits.schemas.habit_schema import CreateHabitSchema, HabitSchema

def post_habit(db: Session, payload: CreateHabitSchema):
    try:
        habit = Habit(
            user_id=payload.user_id,
            name=payload.name,
            frequency=payload.frequency,
            is_active=payload.is_active,
            color=payload.color,
            icon=payload.icon if payload.icon is not None else 'check_circle',
        )
        
        db.add(habit)
        db.flush()
        habit_id = habit.id
        db.commit()        
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={'success': True, 'id': habit_id})
    except Exception:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={'success': False, 'message': 'Failed to create habit'})
        
        
def fetch_habits(db: Session, user_id: int):
    try:
        habits_query = db.query(
            Habit.id,
            Habit.user_id,
            Habit.name,
            Habit.frequency,
            Habit.is_active,
            Habit.icon,
            Habit.color,
        ).filter(Habit.user_id == user_id)  
        habits = []
        
        for habit in habits_query:
            start, end = get_date_periods(frequency=habit.frequency)
            completed = db.query(
                exists().where(
                    HabitLog.habit_id == habit.id,
                    HabitLog.user_id == habit.user_id,
                    HabitLog.completed_at >= start,
                    HabitLog.completed_at < end
                )
            ).scalar()
            
            
            habits.append(
                HabitSchema(
                    id=habit.id,
                    user_id=habit.user_id,
                    name=habit.name,
                    frequency=habit.frequency,
                    is_active=habit.is_active,
                    icon=habit.icon,
                    color=habit.color,
                    is_completed=bool(completed),
                    is_required=bool(habit.is_active) and not completed
                )
            )
        
        return  {"success": True, "habits": habits}
    except Exception:
        raise HTTPException(status_code=500, detail='Failed to fetch habits')
        

def get_date_periods(frequency: str):
    return get_periods()[frequency]
