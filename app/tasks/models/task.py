from datetime import datetime

from sqlalchemy import DateTime, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    priority: Mapped[str] = mapped_column(
        Enum('low', 'medium', 'high'), nullable=False, server_default='medium'
    )
    status: Mapped[str] = mapped_column(
        Enum('pending', 'in_progress', 'completed'),
        nullable=False,
        server_default='pending',
    )
    due_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
