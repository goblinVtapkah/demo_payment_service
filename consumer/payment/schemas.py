from decimal import Decimal
from uuid import UUID
from typing import Any

from pydantic import BaseModel, Field

class Payload(BaseModel):
	webhook_url: str
	cost: Decimal
	currency: str
	description: str
	metadata_json: dict[str, Any]

class PaymentsNewMessage(BaseModel):
	idempotency_key: UUID = Field(alias="Idempotency-Key")
	payload: Payload
	completed_set_status: bool = False
	attempt: int = 0