from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

class TaskSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    title: str
    priority: Literal['low', 'medium', 'high']
    status: Literal['pending', 'in_progress', 'completed']
    due_date: datetime | None