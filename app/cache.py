from cachetools import TTLCache, cached
from typing import Any

# simple in-memory TTL cache: keys -> values, TTL in seconds (tune as needed)
DEFAULT_CACHE = TTLCache(maxsize=1000, ttl=10)  # cache for 10s by default


def cached_with_ttl(ttl: int):
    """Decorator factory to create a TTL cached function."""
    cache = TTLCache(maxsize=1000, ttl=ttl)
    def decorator(fn):
        return cached(cache)(fn)
    return decorator
