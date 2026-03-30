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
    # ✅ Consolidated model registration and table creation
    from models import Base
    from db.session import engine
    
    try:
        from utils.db_check_startup import check_db_connectivity
        db_ok = await check_db_connectivity()
        
        if not db_ok:
            print("⚠️ WARNING: Database check failed during startup. Proceeding anyway (will retry on first request).")
        
        async with engine.begin() as conn:
            # This is safe to run multiple times; it won't drop existing data
            await conn.run_sync(Base.metadata.create_all)
        print("✅ [DB_GUARD] Schema verification complete: Tables are ready.")
    except Exception as e:
        print(f"⚠️ Non-critical database initialization error: {str(e)}")
        print("💡 The app will attempt to connect again during the first API request.")
        
    yield


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
