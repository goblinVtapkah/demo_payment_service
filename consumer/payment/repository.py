from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select

from .models import Payment
from .enums import Status


class PaymentRepository:

    def set_status(self, payment: Payment, status: Status) -> None:
        payment.status = status

    async def get_by_idempotency_key(
		self,
		session: AsyncSession,
		idempotency_key: UUID,
    ) -> Payment | None:
        result = await session.execute(
            select(Payment).where(Payment.idempotency_key == idempotency_key)
        )

        return result.scalar_one_or_none()