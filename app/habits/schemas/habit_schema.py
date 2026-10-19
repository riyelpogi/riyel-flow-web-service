from typing import Literal

from pydantic import BaseModel, Field


class CreateHabitSchema(BaseModel):
    user_id: int
    name: str = Field(min_length=1, max_length=100)
    frequency: Literal['daily', 'weekly', 'monthly'] = 'daily'
    color: str = Field(default='#6366F1', max_length=7)
    icon: str | None = Field(default=None, max_length=50)
    is_active: Literal[0, 1] = 1

class HabitSchema(BaseModel):
    id: int = 0
    user_id: int
    name: str
    icon: str = 'check_circle'
    color: str = '#6366F1'
    frequency: str = 'daily'
    is_active: int = 1
    is_required: bool = False
    is_completed: bool = False
