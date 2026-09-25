from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from core.config import get_settings


x_api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False,
)
settings = get_settings()

async def verify(
    x_api_key: str | None = Security(x_api_key_header),
) -> None:
    if x_api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-API-Key header is required",
        )

    if x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-API-Key header is invalid",
        )