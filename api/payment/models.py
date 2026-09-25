from uuid import UUID
from typing import Any
from decimal import Decimal
from datetime import datetime

from .enums import Currency, Status
from sqlalchemy import String, Numeric, Enum, Text, JSON, Uuid, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base



class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    cost: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    
    currency: Mapped[Currency] = mapped_column(Enum(Currency), nullable=False)

    description: Mapped[str] = mapped_column(Text, nullable=False)

    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

    status: Mapped[Status] = mapped_column(Enum(Status), nullable=False, default=Status.PENDING)

    idempotency_key: Mapped[UUID] = mapped_column(Uuid, nullable=False, unique=True)

    webhook_url: Mapped[str] = mapped_column(String(2048), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    outbox: Mapped["Outbox | None"] = relationship(
        "Outbox",
        back_populates="payment",
        uselist=False,
        cascade="all, delete-orphan",
    )