"""Test Caches"""
import datetime
import tempfile
import unittest

from gs.cache import Cache, FileCache, MemoryCache, get_cache


class TestCache(unittest.TestCase):
    """Test Caches"""

    def test_unknown_cache(self):
        """Asserts uknown cache type raises exception"""
        with self.assertRaises(Exception):
            get_cache('unknown')

    def test_memory_cache(self):
        """Test memory cache"""
        cache = get_cache('memory')
        self._test_cache(cache, MemoryCache)

    def test_file_cache(self):
        """Test file cache"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = get_cache(f'path://{tmpdir}')
            self._test_cache(cache, FileCache)

    def _test_cache(self, cache: Cache, class_type):
        self.assertIsInstance(cache, class_type)
        cache.set('test_key', 'test_value')
        self.assertEqual(cache.get('test_key'), 'test_value')

        cache.set('test_key2', 'test_value2', datetime.timedelta(seconds=-1))
        self.assertIsNone(cache.get('test_key2'))
