"""Generic cache module."""

from .file_cache import FileCache
from .memory_cache import MemoryCache
from .cache_protocol import Cache


def get_cache(connection_string: str) -> Cache:
    for cache in [MemoryCache, FileCache]:
        instance = cache().parse(connection_string)
        if instance:
            return instance
    raise Exception("Cache not found")
