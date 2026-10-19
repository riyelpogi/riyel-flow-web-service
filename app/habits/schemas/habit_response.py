from pydantic import BaseModel

from app.habits.schemas.habit_schema import HabitSchema


class HabitsResponse(BaseModel):
    success: bool
    habits: list[HabitSchema]
