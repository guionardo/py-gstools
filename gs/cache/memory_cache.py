"""Memory Cache"""
import datetime
import logging
from typing import Union

from .cache_protocol import Cache


class MemoryCache(Cache):
    """Memory Cache"""

    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.cache = {}

    def get(self, key: str) -> Union[str, None]:
        if key in self.cache:
            value, valid_until = self.cache[key]
            if valid_until > datetime.datetime.now():
                return value
            del self.cache[key]
        return None

    def set(self, key: str, value: str,
            ttl: datetime.timedelta = datetime.timedelta(seconds=0)) -> None:
        valid_until = datetime.datetime(datetime.MAXYEAR, 1, 1) if ttl.total_seconds(
        ) == 0 else datetime.datetime.now() + ttl

        self.cache[key] = (value, valid_until)

    def parse(self, connection_string: str) -> "MemoryCache":
        if connection_string == "memory":
            self.log.info('Initialized')
            return self
        return False
