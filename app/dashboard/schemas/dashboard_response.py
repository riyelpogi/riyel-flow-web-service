from datetime import date

from pydantic import BaseModel

from app.dashboard.schemas.today_progress_schema import TodayProgressSchema
from app.habits.schemas.habit_schema import HabitSchema
from app.tasks.schemas import TaskSchema

class DashboardResponse(BaseModel):
    success: bool
    date: date
    today_progress: TodayProgressSchema
    tasks: list[TaskSchema]
    habits: list[HabitSchema]
