import asyncio

from faststream.rabbit import RabbitBroker
from core.config import get_settings

settings = get_settings()

broker = RabbitBroker(settings.rabbitmq_url)

async def broker_connect(retries = 5, delay = 5):
    for attempt in range(retries):
        try:
            await broker.connect()
            return
        except:
            if attempt == retries:
                raise

            await asyncio.sleep(delay)