
from pydantic import BaseModel



class TodayProgressSchema(BaseModel):
    total_tasks: int
    total_task_completed: int
    total_habits: int
    total_habit_completed: int
    total: int
    completed: int
    percentage: float
