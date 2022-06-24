"""Cache Protocol"""

import datetime
from typing import Protocol, Union


class Cache(Protocol):
    """Cache Protocol"""

    def get(self, key: str) -> Union[str, None]:
        """Return value or None if not found."""

    def set(self, key: str, value: str,
            ttl: datetime.timedelta = datetime.timedelta(seconds=0)) -> None:
        """Set value with time to live"""

    def parse(self, connection_string: str) -> 'Cache':
        """Parse connection string and return instance of Cache if valid."""
