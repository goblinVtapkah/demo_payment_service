from uuid import UUID
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select

from .models import Outbox
from .enums import Type


class OutboxRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        

    async def get_oldest(self) -> Outbox | None:
        result = await self.session.execute(
            select(Outbox)
            .order_by(Outbox.created_at)
            .limit(1)
        )

        return result.scalar_one_or_none()
    

    async def create(
        self,
        idempotency_key: UUID,
        message_type: Type,
        payload: dict[str, Any],
    ) -> Outbox:
        outbox = Outbox(
            idempotency_key=idempotency_key,
            message_type=message_type,
            payload=payload,
        )

        self.session.add(outbox)

        return outbox

    async def delete(
        self,
        outbox: Outbox,
    ) -> None:
        await self.session.delete(outbox)