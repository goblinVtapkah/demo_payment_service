import asyncio
from random import randint
from requests import post

from sqlalchemy.ext.asyncio import AsyncSession

from .repository import PaymentRepository
from .schemas import PaymentsNewMessage
from .enums import Status


class PaymentService:
    def __init__(self):
        self.repository = PaymentRepository()

    async def process_emulate(self):
        await asyncio.sleep(randint(2, 5))
        return Status.SUCCEEDED if randint(0, 9) else Status.FAILED

    async def process_payment(self, session: AsyncSession, message: PaymentsNewMessage) -> None:

        payment = await self.repository.get_by_idempotency_key(session, message.idempotency_key)

        if payment is None:
            return Exception("Payment not found by Idempotency-Key.")

        if message.completed_set_status and payment.status == Status.PENDING:
            raise Exception("Payment status already setted")
        elif not message.completed_set_status and payment.status == Status.PENDING:
            response_status = await self.process_emulate()
            self.repository.set_status(payment, response_status)
            await session.commit()
            message.completed_set_status = True

        post(
            message.payload.webhook_url,
            headers={
                "Content-Type": "application/json",
            },
            json={
                "cost": str(payment.cost),
                "description": payment.description,
                "created_at": str(payment.created_at),
                "updated_at": str(payment.updated_at),
                "status": payment.status,
            },
            timeout=20,
        )