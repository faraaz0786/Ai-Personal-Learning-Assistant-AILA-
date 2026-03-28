from typing import Any

from fastapi.responses import JSONResponse

from core.logging import request_id_ctx_var


def serialize_exception(e: Exception) -> dict[str, str]:
    """Safely serialize an exception for JSON responses, preventing un-serializable objects."""
    return {
        "type": e.__class__.__name__,
        "message": str(e),
    }


def safe_error_response(
    status_code: int,
    code: str,
    message: str,
    details: Any = None,
) -> JSONResponse:
    """Standardize JSON error responses, guaranteeing essential fields like request_id."""
    request_id = request_id_ctx_var.get()

    content = {
        "error": {
            "code": code,
            "message": message,
            "details": details or {},
        }
    }

    headers = {}
    if request_id:
        headers["X-Request-ID"] = request_id

    return JSONResponse(status_code=status_code, content=content, headers=headers)
