"""Generic cache module."""

from .cache_protocol import Cache
from .file_cache import FileCache
from .memory_cache import MemoryCache
from .redis_cache import RedisCache


def get_cache(connection_string: str) -> Cache:
    """Get cache instance from connection string."""
    for cache in [MemoryCache, FileCache, RedisCache]:
        instance = cache().parse(connection_string)
        if instance:
            return instance
    raise Exception("Cache not found")
