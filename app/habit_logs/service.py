import logging
from datetime import datetime, time

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.habit_logs.models.habit_log import HabitLog
from app.habit_logs.schemas import CreateHabitLogSchema
from app.habits.models.habit import Habit

logger = logging.getLogger(__name__)


def fetch_habit_logs(db: Session, user_id: int, habit_id: int | None = None):
    try:
        query = db.query(HabitLog).filter(HabitLog.user_id == user_id)
        if habit_id is not None:
            query = query.filter(HabitLog.habit_id == habit_id)

        logs = query.order_by(HabitLog.completed_at.desc(), HabitLog.id.desc()).all()
        return {
            'success': True,
            'habit_logs': [
                {
                    'id': log.id,
                    'habit_id': log.habit_id,
                    'user_id': log.user_id,
                    'encode_date': log.encode_date,
                    'completed_at': log.completed_at,
                    'log_date': log.completed_at.date() if log.completed_at else None,
                }
                for log in logs
            ],
        }
    except Exception:
        logger.exception('Failed to fetch habit logs')
        raise HTTPException(status_code=500, detail='Failed to fetch habit logs')


def post_habit_log(db: Session, payload: CreateHabitLogSchema):
    try:
        habit = db.query(Habit).filter(Habit.id == payload.habit_id).first()
        if habit is None:
            raise HTTPException(status_code=404, detail='Habit not found')

        log = HabitLog(
            habit_id=habit.id,
            user_id=habit.user_id,
            encode_date=datetime.now(),
            completed_at=datetime.combine(payload.log_date, time.min),
        )
        db.add(log)
        db.flush()
        log_id = log.id
        db.commit()
        return {'success': True, 'id': log_id} 
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        logger.exception('Failed to create habit log')
        raise HTTPException(status_code=500, detail='Failed to create habit log')
