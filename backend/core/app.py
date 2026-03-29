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
    async def root() -> dict[str, str]:
        return {"message": "AILA backend is running."}

    @app.get("/metrics", tags=["monitor"])
    async def get_metrics() -> dict:
        return metrics_tracker.snapshot()

    return app
