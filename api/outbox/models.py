from uuid import UUID
from typing import Any
from datetime import datetime

from .enums import Type
from sqlalchemy import Enum, JSON, Uuid, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base



class Outbox(Base):
    __tablename__ = "outboxes"

    idempotency_key: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey(
            "payments.idempotency_key",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
        primary_key=True,
    )

    message_type: Mapped[Type] = mapped_column(Enum(Type), nullable=False)

    payload: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    payment: Mapped["Payment"] = relationship(
        "Payment",
        back_populates="outbox",
    )