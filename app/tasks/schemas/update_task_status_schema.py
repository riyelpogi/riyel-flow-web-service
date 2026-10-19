from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

class UpdateTaskStatusSchema(BaseModel):
    status: Literal['pending', 'in_progress', 'completed']
