from datetime import datetime
from decimal import Decimal
from uuid import UUID
from .enums import Currency, Status
from typing import Any

from pydantic import BaseModel, ConfigDict

class PaymentCreate(BaseModel):
    cost: Decimal
    currency: Currency
    description: str
    metadata_json: dict[str, Any]
    webhook_url: str


class PaymentResponse(BaseModel):
    id: int
    status: Status
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaymentFullResponse(BaseModel):
    id: int
    cost: Decimal
    currency: Currency
    description: str
    metadata_json: dict[str, Any]
    status: Status
    idempotency_key: UUID
    webhook_url: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)