import contextvars
from contextlib import contextmanager
from time import perf_counter

# Stores isolated timing contexts for the current active async request
timing_metrics: contextvars.ContextVar[dict[str, int]] = contextvars.ContextVar(
    "timing_metrics", default={}
)


class TimingTracker:
    """
    Tracks sub-millisecond durations of granular operations (DB, AI, Cache)
    during a request's lifecycle using ContextVars to avoid explicitly passing state.
    """

    @contextmanager
    def measure(self, name: str):
        """Context manager to auto-measure arbitrary code blocks."""
        metrics = timing_metrics.get().copy()
        if not metrics:
            metrics = {"db": 0, "ai": 0, "cache": 0}
            timing_metrics.set(metrics)
            
        start = perf_counter()
        try:
            yield
        finally:
            duration = int((perf_counter() - start) * 1000)
            # Fetch latest again in case it was mutated deeply
            latest_metrics = timing_metrics.get().copy()
            latest_metrics[name] = latest_metrics.get(name, 0) + duration
            timing_metrics.set(latest_metrics)

# Global helper instance
timing_tracker = TimingTracker()
