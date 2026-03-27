import logging
from time import perf_counter

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.core.error_utils import safe_error_response
from app.core.metrics import metrics_tracker
from app.core.timing import timing_metrics
from app.core.exceptions import AppError


logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that records purely structured JSON logs about the request lifecycle,
    measuring endpoint latency and tracking metrics.
    """
    async def dispatch(self, request: Request, call_next) -> Response:
        
        # Don't log health or metrics probes to avoid spamming the log stream
        if request.url.path in ["/api/v1/health", "/api/v1/health/db", "/api/v1/health/redis", "/metrics"]:
            try:
                return await call_next(request)
            except AppError:
                raise
            except Exception as e:
                logger.error("Error in health check/metrics endpoint", exc_info=e)
                return safe_error_response(500, "INTERNAL_SERVER_ERROR", "An unexpected error occurred.")
            
        start_time = perf_counter()
        method = request.method
        path = request.url.path
        client_ip = request.client.host if request.client else "unknown"

        # Initialize the deep request timing metrics context
        timing_metrics.set({"db": 0, "ai": 0, "cache": 0})

        # Increment global request count metric
        metrics_tracker.increment_request()

        logger.info(
            "Request started",
            extra={
                "endpoint": path,
                "method": method,
                "client_ip": client_ip,
            }
        )
        
        try:
            response = await call_next(request)
            status_code = response.status_code
        except AppError:
            raise
        except Exception as e:
            status_code = 500
            logger.error("Unhandled exception in LoggingMiddleware downstream", exc_info=e)
            response = safe_error_response(
                status_code=status_code,
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred processing the request.",
            )
        finally:
            duration_ms = int((perf_counter() - start_time) * 1000)
            
            # Observe total latency in global metrics
            metrics_tracker.observe_latency(duration_ms)

            # Extract the deeply traced breakdown
            breakdown = timing_metrics.get()
            breakdown["total"] = duration_ms

            logger.info(
                "Request completed",
                extra={
                    "endpoint": path,
                    "method": method,
                    "status_code": status_code,
                    "duration_ms": duration_ms,
                    "timings": breakdown,
                }
            )

        return response
