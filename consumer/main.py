from faststream import FastStream

from payment import subscribers
from payment.topology import (
    payments_retry_1,
    payments_retry_2,
    payments_retry_3,
    payments_dlq,
)

from broker.broker import broker

from core.logging import setup_logging

app = FastStream(broker)

setup_logging()


@app.after_startup
async def publish_message():
    await broker.declare_queue(payments_retry_1)
    await broker.declare_queue(payments_retry_2)
    await broker.declare_queue(payments_retry_3)
    dlq_queue = await broker.declare_queue(payments_dlq)

    await dlq_queue.bind("payments.dlx", routing_key="dlq")