"""LLM response caching service backed by Redis."""

import hashlib
import json
import logging

import redis.asyncio as redis

from app.core.redis import get_client
from app.core.timing import timing_tracker

logger = logging.getLogger(__name__)


# TTL constants (seconds)
TTL_EXPLAIN = 60 * 60 * 24      # 24 hours
TTL_SUMMARY = 60 * 60 * 24      # 24 hours
TTL_QUIZ = 60 * 60 * 12         # 12 hours
TTL_RECOMMENDATIONS = 60 * 60 * 6  # 6 hours

_TTL_MAP: dict[str, int] = {
    "explain": TTL_EXPLAIN,
    "summary": TTL_SUMMARY,
    "quiz": TTL_QUIZ,
    "recommendations": TTL_RECOMMENDATIONS,
}


def _normalize(text: str) -> str:
    """Lowercase, strip, collapse whitespace."""
    return " ".join(text.lower().split())


def generate_cache_key(feature: str, **inputs: str) -> str:
    """Build a stable, deterministic cache key.

    Format: ``ai_cache:{feature}:{sha256(sorted_inputs)}``
    """
    parts = sorted(f"{k}={_normalize(str(v))}" for k, v in inputs.items())
    raw = "|".join(parts)
    digest = hashlib.sha256(raw.encode()).hexdigest()[:16]
    return f"ai_cache:{feature}:{digest}"


def get_ttl(feature: str) -> int:
    """Return the TTL for a given feature, default 1 hour."""
    return _TTL_MAP.get(feature, 3600)


class AICacheService:
    """Thin wrapper around Redis for LLM response caching."""

    async def get_cached(self, key: str) -> dict | None:
        """Return the cached JSON dict or None on miss / error."""
        with timing_tracker.measure("cache"):
            client = get_client()
            if client is None:
                return None
            try:
                raw = await client.get(key)
                if raw is None:
                    return None
                data = json.loads(raw)
                logger.debug("Cache HIT: %s", key)
                return data
            except (redis.RedisError, json.JSONDecodeError) as exc:
                logger.warning("Cache get error for %s: %s", key, exc)
                return None

    async def set_cached(self, key: str, value: dict, ttl: int) -> None:
        """Store a validated response dict in Redis with a TTL."""
        with timing_tracker.measure("cache"):
            client = get_client()
            if client is None:
                return
            try:
                serialized = json.dumps(value, default=str)
                await client.setex(key, ttl, serialized)
                logger.debug("Cache SET: %s (ttl=%ds)", key, ttl)
            except (redis.RedisError, TypeError) as exc:
                logger.warning("Cache set error for %s: %s", key, exc)

    async def acquire_lock(self, key: str, timeout: int = 30) -> bool:
        """Acquire a distributed lock for cache stampede prevention."""
        client = get_client()
        if client is None:
            return True  # Proceed gracefully if Redis is unresponsive
        try:
            lock_key = f"{key}:lock"
            # Set integer 1 if key doesn't exist, expiring in 'timeout'
            acquired = await client.set(lock_key, "1", nx=True, ex=timeout)
            return bool(acquired)
        except redis.RedisError as exc:
            logger.warning("Lock acquire error for %s: %s", key, exc)
            return True

    async def release_lock(self, key: str) -> None:
        """Release the distributed lock."""
        client = get_client()
        if client is None:
            return
        try:
            lock_key = f"{key}:lock"
            await client.delete(lock_key)
        except redis.RedisError as exc:
            logger.warning("Lock release error for %s: %s", key, exc)

    async def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching a specific pattern."""
        client = get_client()
        if client is None:
            return 0
        try:
            count = 0
            async for matched_key in client.scan_iter(match=pattern):
                await client.delete(matched_key)
                count += 1
            if count > 0:
                logger.info("Invalidated %d cache keys matching '%s'", count, pattern)
            return count
        except redis.RedisError as exc:
            logger.warning("Cache invalidation error for %s: %s", pattern, exc)
            return 0
