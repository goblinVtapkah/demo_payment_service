from uuid import UUID

from fastapi import APIRouter, Depends, status, Header, Security
from fastapi.responses import JSONResponse

from auth.dependencies import verify

from .service import PaymentService
from .dependencies import get_payment_service
from .schemas import PaymentCreate, PaymentResponse, PaymentFullResponse


router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
    default_response_class=JSONResponse,
    dependencies=[Security(verify)]
)


@router.post(
    "",
    response_model=PaymentResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def create_payment(
    data: PaymentCreate,
    idempotency_key: UUID = Header(...),
    service: PaymentService = Depends(get_payment_service),
) -> PaymentResponse:
    return await service.create_payment(data, idempotency_key)


@router.get(
    "/{payment_id}",
    response_model=PaymentFullResponse,
    status_code=status.HTTP_200_OK,
)
async def get_payment(
    payment_id: int,
    service: PaymentService = Depends(get_payment_service),
) -> PaymentFullResponse:
    return await service.get_payment(payment_id)