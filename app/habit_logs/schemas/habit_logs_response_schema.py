
from pydantic import BaseModel

from .habit_log_schema import HabitLogSchema


class HabitLogsResponseSchema(BaseModel):
    success: bool
    habit_logs: list[HabitLogSchema]
