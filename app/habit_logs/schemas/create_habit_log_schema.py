from datetime import date

from pydantic import BaseModel, Field


class CreateHabitLogSchema(BaseModel):
    habit_id: int = Field(gt=0)
    log_date: date
