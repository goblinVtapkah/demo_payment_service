from uuid import UUID

from fastapi import HTTPException, status

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from outbox.repository import OutboxRepository
from outbox.enums import Type

from .repository import PaymentRepository
from .schemas import PaymentCreate
from .models import Payment


class PaymentService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = PaymentRepository(session)
        self.outboxRepository = OutboxRepository(session)

    async def create_payment(self, data: PaymentCreate, idempotency_key: UUID) -> Payment:

        try:
            async with self.session.begin():
                payment = await self.repository.create(data, idempotency_key)
                await self.outboxRepository.create(
                    idempotency_key,
                    Type.PAYMENT,
                    {
                        "webhook_url": payment.webhook_url,
                        "cost": str(payment.cost),
                        "currency": payment.currency,
                        "description": payment.description,
                        "metadata_json": payment.metadata_json,
                    },
                )


            return payment
        except IntegrityError as e:
            if getattr(e.orig, "sqlstate", None) == "23505":
                payment = await self.repository.get_by_idempotency_key(idempotency_key)

                if payment.cost == data.cost and \
                    payment.description == data.description and \
                    payment.metadata_json == data.metadata_json and \
                    payment.currency == data.currency:
                        return payment
                else:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Idempotency-key has already been used with different request parameters",
                    )
            
            raise

    async def get_payment(self, payment_id: int) -> Payment:

        payment = await self.repository.get_by_id(payment_id)

        if payment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found payment with that payment_id",
            )

        return payment