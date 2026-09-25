from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select

from .models import Payment
from .schemas import PaymentCreate


class PaymentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, payment_id: int) -> Payment | None:
        result = await self.session.execute(
            select(Payment).where(Payment.id == payment_id)
        )

        return result.scalar_one_or_none()
    

    async def get_by_idempotency_key(self, idempotency_key: UUID) -> Payment | None:
        result = await self.session.execute(
            select(Payment).where(Payment.idempotency_key == idempotency_key)
        )

        return result.scalar_one_or_none()
    

    async def create(self, data: PaymentCreate, idempotency_key: UUID) -> Payment:
        payment = Payment(
            cost=data.cost,
            currency=data.currency,
            description=data.description,
            metadata_json=data.metadata_json,
            webhook_url=data.webhook_url,
            idempotency_key=idempotency_key,
        )

        self.session.add(payment)

        return payment