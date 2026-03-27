import json
import logging
import traceback
from contextvars import ContextVar
from datetime import datetime, timezone


# Context variable to hold the request ID across the async request lifecycle
request_id_ctx_var: ContextVar[str | None] = ContextVar("request_id", default=None)


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Inject request_id if available in context
        request_id = request_id_ctx_var.get()
        if request_id:
            log_data["request_id"] = request_id
            
        # Add custom extra attributes passed to logger (e.g. logger.info("msg", extra={"user": "abc"}))
        for key, value in record.__dict__.items():
            if key not in logging.LogRecord(None, None, "", 0, "", (), None, None).__dict__ and key not in log_data:
                log_data[key] = value

        # Formatter handles exceptions
        if record.exc_info:
            log_data["error"] = self.formatException(record.exc_info)
            # You can also add full traceback if needed
            log_data["traceback"] = "".join(traceback.format_exception(*record.exc_info))

        return json.dumps(log_data)


def configure_logging(level: str) -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    
    root_logger = logging.getLogger()
    root_logger.setLevel(level.upper())
    
    # Remove existing handlers to avoid duplicates
    if root_logger.hasHandlers():
        root_logger.handlers.clear()
        
    root_logger.addHandler(handler)
    
    # Silence third-party verbose loggers (like httpx or sqlalchemy if needed)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
