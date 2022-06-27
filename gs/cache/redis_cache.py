"""Redis Cache"""
import datetime
import logging
from typing import Union

import redis.utils

from .cache_protocol import Cache


class RedisCache(Cache):
    """Redis Cache"""

    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.redis: redis.Redis = None

    def get(self, key: str) -> Union[str, None]:
        """Return value or None if not found."""
        value = self.redis.get(key)
        if isinstance(value, bytes):
            value = value.decode('utf-8')
        return value

    def set(self, key: str, value: str,
            ttl: datetime.timedelta = datetime.timedelta(seconds=0)) -> None:
        """Set value with time to live"""
        if ttl.total_seconds() > 0:
            self.redis.set(key, value, ex=int(ttl.total_seconds()))
        elif ttl.total_seconds() == 0:
            self.redis.set(key, value)

    def parse(self, connection_string: str) -> 'Cache':
        """Parse connection string and return instance of Cache if valid."""
        if not connection_string.startswith('redis://'):
            return None

        self.redis = redis.utils.from_url(connection_string)
        self.log.info('Initialized')
        return self
