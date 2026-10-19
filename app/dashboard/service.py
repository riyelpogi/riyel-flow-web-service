import logging
from datetime import date as Date
from app.utils.date_periods import get_periods

from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.habit_logs.models.habit_log import HabitLog
from app.habits.models.habit import Habit
from app.habits.schemas.habit_schema import HabitSchema
from app.tasks.models.task import Task

logger = logging.getLogger(__name__)


def fetch_dashboard(db: Session, user_id: int, date: Date | None = None):
    try:
        periods = get_periods(date)
        today, tomorrow = periods['daily']
        week_start = periods['weekly'][0]
        month_start, next_month = periods['monthly']

        tasks = db.query(Task).filter(
            Task.user_id == user_id,
            or_(Task.due_date.is_(None), Task.due_date < tomorrow),
        ).order_by(Task.id.desc()).all()
        habits = db.query(Habit).filter(
            Habit.user_id == user_id, Habit.is_active == 1,
        ).order_by(Habit.id.desc()).all()

        logs = db.query(HabitLog.habit_id, HabitLog.completed_at).filter(
            HabitLog.user_id == user_id,
            HabitLog.completed_at >= min(week_start, month_start),
            HabitLog.completed_at < max(tomorrow, periods['weekly'][1], next_month),
        ).all()
        completions = {}
        for log in logs:
            completions.setdefault(log.habit_id, []).append(log.completed_at)

        required_habits = []
        completed_habits = 0
        for habit in habits:
            start, end = periods[habit.frequency]
            completed = any(
                start <= timestamp < end
                for timestamp in completions.get(habit.id, [])
            )
            if completed:
                completed_habits += 1
            else:
                required_habits.append(HabitSchema(
                    id=habit.id, user_id=habit.user_id, name=habit.name,
                    frequency=habit.frequency, icon=habit.icon, color=habit.color,
                    is_active=habit.is_active, is_completed=False, is_required=True,
                ))

        completed_tasks = sum(task.status == 'completed' for task in tasks)
        total = len(tasks) + len(habits)
        completed = completed_tasks + completed_habits
        return {
            'success': True,
            'date': today.date(),
            'today_progress': {
                'total_tasks': len(tasks), 'total_task_completed': completed_tasks,
                'total_habits': len(habits), 'total_habit_completed': completed_habits,
                'total': total, 'completed': completed,
                'percentage': round(completed / total * 100, 2) if total else 0.0,
            },
            'tasks': [task for task in tasks if task.status != 'completed'],
            'habits': required_habits,
        }
    except Exception:
        logger.exception('Failed to fetch dashboard')
        raise HTTPException(status_code=500, detail='Failed to fetch dashboard')
