from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.exceptions import AppError
from app.core.handlers import (
    app_error_handler,
    unhandled_exception_handler,
    validation_error_handler,
)
from app.core.logging import configure_logging
from app.core import redis as redis_client
from app.core.metrics import metrics_tracker
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.rate_limiter import RateLimiterMiddleware
from app.middleware.request_id import RequestIdMiddleware
from app.middleware.security import SecurityHeadersMiddleware
from app.middleware.session import SessionContextMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle events."""
    await redis_client.connect()
    yield
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

    # Note: Middlewares are executed roughly physically bottom-to-top 
    # for the request phase, so RequestId is the outermost (earliest).
    app.add_middleware(RateLimiterMiddleware)
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
    async def root() -> dict[str, str]:
        return {"message": "AILA backend is running."}

    @app.get("/metrics", tags=["monitor"])
    async def get_metrics() -> dict:
        return metrics_tracker.snapshot()

    return app
