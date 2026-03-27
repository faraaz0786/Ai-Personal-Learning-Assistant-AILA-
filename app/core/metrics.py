import logging
from collections import defaultdict
from threading import Lock

logger = logging.getLogger(__name__)


class MetricsTracker:
    """
    In-memory atomic metrics tracker to monitor application health
    and AI service utilization without external dependencies.
    """
    def __init__(self):
        self._lock = Lock()
        self.request_count: int = 0
        self.error_count: int = 0
        
        # Latency tracking (moving average simply computed for the runtime)
        self.total_latency_ms: int = 0
        
        # AI usage tracking
        self.ai_call_count: dict[str, int] = defaultdict(int)
        self.ai_cache_hits: dict[str, int] = defaultdict(int)
        self.ai_cache_misses: dict[str, int] = defaultdict(int)
        self.ai_success_count: dict[str, int] = defaultdict(int)
        self.ai_failure_count: dict[str, int] = defaultdict(int)

    def increment_request(self) -> None:
        with self._lock:
            self.request_count += 1

    def increment_error(self) -> None:
        with self._lock:
            self.error_count += 1

    def observe_latency(self, duration_ms: int) -> None:
        with self._lock:
            self.total_latency_ms += duration_ms

    def record_ai_call(self, feature: str, cache_hit: bool, successful: bool = True) -> None:
        with self._lock:
            self.ai_call_count[feature] += 1
            if cache_hit:
                self.ai_cache_hits[feature] += 1
            else:
                self.ai_cache_misses[feature] += 1
                
            if successful:
                self.ai_success_count[feature] += 1
            else:
                self.ai_failure_count[feature] += 1

    def snapshot(self) -> dict:
        """Return the current metrics safely."""
        with self._lock:
            avg_latency = 0
            if self.request_count > 0:
                avg_latency = round(self.total_latency_ms / self.request_count, 2)
                
            return {
                "system": {
                    "request_count": self.request_count,
                    "error_count": self.error_count,
                    "avg_latency_ms": avg_latency,
                },
                "ai_usage": dict(self.ai_call_count),
                "ai_performance": {
                    "success": dict(self.ai_success_count),
                    "failure": dict(self.ai_failure_count),
                },
                "cache_efficiency": {
                    "hits": dict(self.ai_cache_hits),
                    "misses": dict(self.ai_cache_misses),
                }
            }

# Singleton instance exported for use across the application
metrics_tracker = MetricsTracker()
