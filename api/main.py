import asyncio

from contextlib import asynccontextmanager

from fastapi import FastAPI

from payment.api import router as payment_router

from database.base import Base
from database.session import engine

from broker.broker import broker, broker_connect

from outbox.worker import OutboxWorker

from core.logging import setup_logging

setup_logging()

worker = OutboxWorker()

@asynccontextmanager
async def lifespan(app: FastAPI):

    await broker_connect()
    worker_task = asyncio.create_task(worker.run())

    yield

    worker.stop()
    await broker.disconnect()
    worker_task.cancel()


app = FastAPI(
    lifespan=lifespan,
    
    title="Payment Service",
    description="API для обработки платежей",
    version="1.0.0",

    root_path="/api/v1",
)


app.include_router(payment_router)