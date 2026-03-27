"""Async Redis client singleton for caching and rate limiting."""

import logging

import redis.asyncio as redis

from app.core.config import get_settings

logger = logging.getLogger(__name__)

_client: redis.Redis | None = None


async def connect() -> None:
    """Initialize the Redis connection pool on app startup."""
    global _client
    settings = get_settings()
    
    _client = redis.from_url(
        settings.redis_url,
        decode_responses=True,
        socket_connect_timeout=2,
        socket_timeout=2,
        retry_on_timeout=True,
    )
    
    try:
        await _client.ping()
        logger.info("Redis connected at %s", settings.redis_url)
    except Exception as exc:
        if settings.environment == "development":
            import fakeredis
            logger.warning("Redis unavailable: %s — falling back to FakeAsyncRedis for development", exc)
            _client = fakeredis.FakeAsyncRedis(decode_responses=True)
        else:
            logger.error("Redis unreachable in %s mode: %s", settings.environment, exc)
            _client = None


async def close() -> None:
    """Close the Redis connection pool on app shutdown."""
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None
        logger.info("Redis connection closed.")


def get_client() -> redis.Redis | None:
    """Return the active Redis client, or None if unavailable."""
    return _client


async def ping() -> bool:
    """Check Redis connectivity. Returns False on any error."""
    if _client is None:
        return False
    try:
        return await _client.ping()
    except redis.RedisError:
        return False
