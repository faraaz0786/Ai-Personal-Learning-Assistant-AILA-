import logging
from api.core.metrics import metrics_tracker

logger = logging.getLogger(__name__)


class AIObserver:
    """
    Observability engine for monitoring AI/LLM events.
    Records metrics to the internal tracker and outputs dedicated structured JSON logs
    for data analysis.
    """
    
    @staticmethod
    def track_generation(
        feature: str,
        latency_ms: int,
        cache_hit: bool,
        tokens_used: int | None = None,
        llm_model: str | None = None,
        successful: bool = True,
    ) -> None:
        """
        Log an AI generation event.
        - Updates global metrics counters
        - Emits a structured log
        """
        # 1. Update internal metrics counters
        metrics_tracker.record_ai_call(feature=feature, cache_hit=cache_hit, successful=successful)
        
        # 2. Emit structured log entry exactly matching requirements
        logger.info(
            "AI generation event",
            extra={
                "event_type": "ai_generation",
                "feature": feature,
                "latency_ms": latency_ms,
                "cache_hit": cache_hit,
                "tokens_used": tokens_used or 0,
                "llm_model": llm_model or "unknown",
                "successful": successful,
            }
        )

# Export singleton pattern standard
ai_observer = AIObserver()
