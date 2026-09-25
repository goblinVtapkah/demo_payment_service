from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import get_session
from .service import PaymentService


def get_payment_service(session: AsyncSession = Depends(get_session)) -> PaymentService:
    return PaymentService(session)