from fastapi import APIRouter, Depends

from core.dependencies import get_health_service
from schemas.common import HealthResponse
from services.health_service import HealthService


router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/health/db", response_model=HealthResponse)
async def database_health_check(
    health_service: HealthService = Depends(get_health_service),
) -> HealthResponse:
    return await health_service.database_health()


@router.get("/health/redis", response_model=HealthResponse)
async def redis_health_check(
    health_service: HealthService = Depends(get_health_service),
) -> HealthResponse:
    return await health_service.redis_health()
