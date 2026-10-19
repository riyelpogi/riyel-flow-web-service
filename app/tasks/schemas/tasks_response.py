from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .task_schema import TaskSchema

class TasksResponse(BaseModel):
    success: bool
    tasks: list[TaskSchema]
