import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from api.core.error_utils import safe_error_response, serialize_exception
from api.core.exceptions import AppError
from api.core.metrics import metrics_tracker


logger = logging.getLogger(__name__)


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    metrics_tracker.increment_error()
    logger.error(
        "Application Error", 
        extra={
            "status_code": exc.status_code,
            "error_code": exc.code,
            "error_message": exc.message,
            "endpoint": request.url.path,
            "method": request.method,
        }
    )
    if exc.code == "LEARN_FAILED":
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.code,
                "message": exc.message,
                "fallback": exc.details.get("fallback", True)
            }
        )

    return safe_error_response(
        status_code=exc.status_code,
        code=exc.code,
        message=exc.message,
        details=exc.details,
    )


async def validation_error_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    metrics_tracker.increment_error()
    
    # Extract clean field-level errors (Pydantic naturally gives serializable dicts)
    # Exclude the raw exception object which may cause JSON errors
    errors = exc.errors()
    clean_errors = [
        {"loc": err.get("loc"), "msg": err.get("msg"), "type": err.get("type")}
        for err in errors
    ]
    
    logger.error(
        "Validation error",
        extra={
            "status_code": 422,
            "error_code": "VALIDATION_ERROR",
            "endpoint": request.url.path,
            "method": request.method,
            "details": clean_errors,
        }
    )
    
    topic_too_short = any(
        err.get("loc", [])[-1:] == ("topic",)
        and err.get("type") == "string_too_short"
        for err in errors
    )

    if topic_too_short:
        return safe_error_response(
            status_code=400,
            code="TOPIC_TOO_SHORT",
            message="Topic input must be at least 3 characters long.",
            details={"fields": clean_errors},
        )

    return safe_error_response(
        status_code=422,
        code="VALIDATION_ERROR",
        message="Request validation failed.",
        details={"fields": clean_errors},
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    metrics_tracker.increment_error()
    logger.error(
        "Unhandled application error",
        exc_info=exc,
        extra={
            "status_code": 500,
            "error_code": "INTERNAL_SERVER_ERROR",
            "endpoint": request.url.path,
            "method": request.method,
            "error": str(exc),
        }
    )
    return safe_error_response(
        status_code=500,
        code="INTERNAL_SERVER_ERROR",
        message="An unexpected error occurred.",
        details=serialize_exception(exc),
    )
