from typing import Literal

from pydantic import BaseModel


class UpdateTaskStatusResponse(BaseModel):
    success: bool
    id: int
    status: Literal['pending', 'in_progress', 'completed']