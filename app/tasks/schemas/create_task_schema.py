from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CreateTaskSchema(BaseModel):
    user_id: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=255)
    priority: Literal['low', 'medium', 'high'] = 'medium'
    status: Literal['pending', 'in_progress', 'completed'] = 'pending'
    due_date: datetime | None = None

    @field_validator('title', mode='before')
    @classmethod
    def trim_title(cls, value):
        return value.strip() if isinstance(value, str) else value
