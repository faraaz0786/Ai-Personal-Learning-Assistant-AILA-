from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import redis as redis_client
from app.schemas.common import HealthResponse


class HealthService:
    def __init__(self, *, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def database_health(self) -> HealthResponse:
        try:
            await self.db_session.execute(text("SELECT 1"))
            return HealthResponse(status="ok", detail="Database connection is healthy.")
        except Exception as exc:
            return HealthResponse(status="error", detail=f"Database connection failed: {exc}")

    async def redis_health(self) -> HealthResponse:
        alive = await redis_client.ping()
        if alive:
            return HealthResponse(status="ok", detail="Redis connection is healthy.")
        return HealthResponse(status="error", detail="Redis is unreachable.")
