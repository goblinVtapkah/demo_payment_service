from sqlalchemy.ext.asyncio import AsyncSession

from payment.publishers import payments_new_publish

from .repository import OutboxRepository

class OutboxService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = OutboxRepository(session)

    async def process(self) -> bool:
        try:
            outbox = await self.repository.get_oldest()
            if outbox:
				
                await payments_new_publish({
					"Idempotency-Key": outbox.idempotency_key,
					"payload": outbox.payload,
                })
                await self.repository.delete(outbox)
                await self.session.commit()
                
                return True

        except:
            await self.session.rollback()

        return False