from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from core.config import get_settings
from core.exceptions import AppError
from core.handlers import (
    app_error_handler,
    unhandled_exception_handler,
    validation_error_handler,
)
from core.logging import configure_logging
from core.metrics import metrics_tracker
from middleware.logging_middleware import LoggingMiddleware
from middleware.request_id import RequestIdMiddleware
from middleware.security import SecurityHeadersMiddleware
from middleware.session import SessionContextMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle events."""
    try:
        from core import redis as redis_client
        import asyncio
        await asyncio.wait_for(redis_client.connect(), timeout=5)
        print("[LIFESPAN] Redis connection initialized.")
    except Exception as e:
        print(f"!! [LIFESPAN] Redis initialization warning: {e}")

    try:
        import asyncio
        from utils.db_check_startup import check_db_connectivity
        # Strict timeout to prevent boot hang
        db_ok = await asyncio.wait_for(check_db_connectivity(), timeout=15)
        
        if not db_ok:
            print("⚠️ WARNING: Database check failed during startup.")
        
        # Explicitly import all models to populate Base.metadata
        from models import Base, SessionModel, ExplanationModel, QuizModel, QuizAttemptModel, TopicModel
        from db.session import engine
        
        print("[DB_GUARD] Verifying schema...")
        async with engine.begin() as conn:
            await asyncio.wait_for(conn.run_sync(Base.metadata.create_all), timeout=20)
        print("[DB_GUARD] Schema verification completed.")
    except asyncio.TimeoutError:
        print("⏳ [DB_GUARD] Database initialization timed out. Proceeding in degraded mode.")
    except Exception as e:
        print(f"!! [DB_GUARD] Database initialization error: {str(e)}")
        
    yield
    
    # Shutdown logic
    from core import redis as redis_client
    await redis_client.close()


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # 🔍 Safe Log masked DB URL for production debugging
    import logging
    logger = logging.getLogger("core.app")
    try:
        masked_host = settings.database_url.split("@")[-1].split("?")[0]
        logger.info(f"⚙️ App Initialized. Database Host: {masked_host}")
    except:
        logger.warning("⚙️ App Initialized. Could not parse database host for logging.")

    # Note: Middlewares are executed roughly physically bottom-to-top 
    # for the request phase, so RequestId is the outermost (earliest).
    app.add_middleware(SessionContextMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)
    
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(RequestIdMiddleware)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

    @app.get("/", tags=["root"])
    @app.head("/", include_in_schema=False)
    async def root() -> dict[str, str]:
        return {"message": "AILA backend is running."}

    @app.get("/metrics", tags=["monitor"])
    async def get_metrics() -> dict:
        return metrics_tracker.snapshot()

    return app
