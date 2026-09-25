from broker.broker import broker
from database.session import AsyncSessionLocal

from .topology import payments_new, payments_dlx
from .schemas import PaymentsNewMessage
from .service import PaymentService
from .publishers import first_try, second_try, third_try

service = PaymentService()


@broker.subscriber(
    queue=payments_new,
    exchange=payments_dlx,
)
async def handle_payments_new_create(message: PaymentsNewMessage):
    message.attempt += 1
    try:
        async with AsyncSessionLocal() as session:
            await service.process_payment(session, message)
    except Exception as e:
        if message.attempt > 3: raise
        if message.attempt == 1: await first_try(message)
        elif message.attempt == 2: await second_try(message)
        elif message.attempt == 3: await third_try(message)