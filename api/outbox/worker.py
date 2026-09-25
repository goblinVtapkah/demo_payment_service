import asyncio

from database.session import AsyncSessionLocal

from .service import OutboxService

class OutboxWorker:
    async def run(self):
        async with AsyncSessionLocal() as session:
            service = OutboxService(session)
            self.cycle = True
            while self.cycle:
                try:
                    result = await service.process()
                    
                    if not result:
                        await asyncio.sleep(60)
                except:
                    await asyncio.sleep(300)

    def stop(self):
        self.cycle = False
        