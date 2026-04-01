from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.config import get_settings


settings = get_settings()
# ✅ Build engine arguments conditionally for SQLite/Postgres compatibility
engine_args = {
    "future": True,
}

if settings.database_url.startswith("postgresql"):
    engine_args.update({
        "pool_pre_ping": True,
        "pool_recycle": 3600,
        "pool_size": 3,
        "max_overflow": 2,
        "connect_args": {
            "command_timeout": 15,
            "ssl": "require",
            "server_settings": {
                "application_name": "AILA-Backend"
            }
        }
    })

engine = create_async_engine(settings.database_url, **engine_args)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise
