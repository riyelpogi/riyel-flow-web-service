from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

class HabitLogSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    habit_id: int
    user_id: int
    encode_date: datetime | None
    completed_at: datetime | None
    log_date: date | None
