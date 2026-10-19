
from sqlalchemy import Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base


class Habit(Base):
    __tablename__ = "habits"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(
            Integer, nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, )
    icon: Mapped[str] = mapped_column(String(50), nullable=False, default='check_circle')
    color: Mapped[str] = mapped_column(String(7), nullable=False, default='#6366F1')
    frequency: Mapped[str] = mapped_column(Enum('daily', 'weekly', 'monthly'), nullable=False, default='daily')
    is_active: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
