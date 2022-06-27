"""Mocking redis"""


class FakeRedis():
    """Fake redis class"""

    def get(self, key: str):
        return {'test_key': b'test_value',
                'test_key2': None}.get(key)

    def set(self, *args, **kwargs):
        ...


def fake_from_url(*args, **kwargs):
    """Fake from_url function"""
    return FakeRedis()
