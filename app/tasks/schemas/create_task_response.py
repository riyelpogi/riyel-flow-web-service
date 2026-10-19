from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

class CreateTaskResponse(BaseModel):
    success: bool
    id: int