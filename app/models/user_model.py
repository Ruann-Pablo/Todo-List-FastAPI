from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.connection import Base
from datetime import datetime, timezone


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, index=True, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    tasks = relationship("Task", back_populates="user")
