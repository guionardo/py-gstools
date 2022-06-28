"""File Cache"""
import datetime
import hashlib
import json
import logging
import os
from typing import Union

from .cache_protocol import Cache


class FileCache(Cache):
    """File Cache"""

    def __init__(self) -> None:
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.info('Initialized')
        self.path = None

    def _filename(self, key: str) -> str:
        hash_name = hashlib.sha1(key.encode('utf-8')).hexdigest()
        return os.path.join(self.path, f'cache_{hash_name}.json')

    def get(self, key: str) -> Union[str, None]:
        filename = self._filename(key)

        if not os.path.isfile(filename):
            return None
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                value, valid_until = json.load(file)
            if valid_until > datetime.datetime.now().timestamp():
                return value
        except Exception as exc:
            self.log.error('Error reading cache file %s: %s', filename, exc)

        os.remove(filename)
        return None

    def set(self, key: str, value: str,
            ttl: datetime.timedelta = datetime.timedelta(seconds=0)) -> None:
        valid_until = datetime.datetime(datetime.MAXYEAR, 1, 1) if ttl.total_seconds(
        ) == 0 else datetime.datetime.now() + ttl
        filename = self._filename(key)
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump((value, valid_until.timestamp()), file)
        except Exception as exc:
            self.log.error('Error writing cache file %s: %s', filename, exc)

    def parse(self, connection_string: str) -> 'Cache':
        """path:str"""
        words = connection_string.split(':', maxsplit=1)
        if len(words) != 2 or words[0] != 'path':
            return None
        path = words[1]
        if not os.path.isdir(path):
            os.makedirs(path, exist_ok=True)
        self.path = path
        return self
