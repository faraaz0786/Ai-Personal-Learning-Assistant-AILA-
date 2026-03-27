import logging
import time

logger = logging.getLogger(__name__)


class CircuitBreakerOpenException(Exception):
    """Raised when the circuit breaker is open and refusing traffic."""
    pass


class CircuitBreaker:
    """
    A basic Circuit Breaker pattern to protect falling services (like LLM APIs)
    from being slammed with requests when they are known to be down.
    """
    def __init__(self, failure_threshold: int = 5, recovery_timeout_sec: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout_sec = recovery_timeout_sec
        self.failure_count = 0
        self.last_failure_time = 0.0
        self.state = "CLOSED"

    def record_failure(self) -> None:
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold and self.state != "OPEN":
            self.state = "OPEN"
            logger.critical("Circuit breaker tripped to OPEN state. Traffic halted.")

    def record_success(self) -> None:
        if self.state != "CLOSED":
            logger.info("Circuit breaker reset to CLOSED. Traffic resuming.")
        self.failure_count = 0
        self.state = "CLOSED"

    def check(self) -> None:
        """Raises CircuitBreakerOpenException if the circuit is OPEN and recovery timeout hasn't passed."""
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout_sec:
                self.state = "HALF_OPEN"
                logger.warning("Circuit breaker transitioning to HALF_OPEN for testing.")
            else:
                raise CircuitBreakerOpenException("Circuit breaker is OPEN. Service temporarily unavailable.")


# Global default instance for the AI Provider layer
ai_circuit_breaker = CircuitBreaker(failure_threshold=5, recovery_timeout_sec=60)
