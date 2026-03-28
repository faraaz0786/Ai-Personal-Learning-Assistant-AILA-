from fastapi import APIRouter

from api.api.v1.router import router as v1_router
from api.core.config import get_settings


settings = get_settings()

api_router = APIRouter(prefix=settings.api_v1_prefix)
api_router.include_router(v1_router)
