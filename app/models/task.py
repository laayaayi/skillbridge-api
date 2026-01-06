from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"), nullable=False, index=True)

    title: Mapped[str] = mapped_column(String(200), nullable=False)

    # وضعیت تسک
    status: Mapped[str] = mapped_column(String(20), default="todo", nullable=False)  # todo / done
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
