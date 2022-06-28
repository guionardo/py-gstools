"""Configuration tests"""
import math
import os
import tempfile
import unittest
from datetime import date, datetime, timedelta
from typing import List

from gs.config import BaseConfig


class SubConfig(BaseConfig):
    """Sample configuration class"""
    ARG_1: int = 10
    ARG_2: str = 'abc'


class Config(BaseConfig):
    """Sample configuration class"""

    INT_ARG: int = 1  # DOCUMENT FOR INT_ARG
    INT_ARG_2: int
    STR_ARG = 'abcd'  # DOCUMENT FOR STR_ARG
    LIST_ARG: List[str] = ['a', 'b', 'c', 'd']
    SUB_CONFIG: SubConfig
    SUB_CONFIGS: List[SubConfig]


class EnvConfig(BaseConfig):
    """Environment based config"""

    TESTING_ALPHA: str = 'alpha'   # ENV:TEST_ALPHA
    TESTING_BETA: str = 'beta'
    TESTING_GAMMA: bool = False     # ENV:TEST_GAMMA


class ConfigTypes(BaseConfig):
    """Types config"""
    INT_ARG: int = 1
    FLOAT_ARG: float = 1.0
    BOOL_ARG: bool = True
    STR_ARG: str = 'abc'
    DATETIME_ARG: datetime
    DATE_ARG: date
    TIMEDELTA_ARG: timedelta


class TestBaseConfig(unittest.TestCase):
    """Test Base Config"""

    def test_config_types(self):
        with self.assertRaises(TypeError):
            cfg = ConfigTypes(INT_ARG=10, FLOAT_ARG=math.pi, BOOL_ARG=False, STR_ARG='abc',
                              DATETIME_ARG=datetime.now(), DATE_ARG=date.today(),
                              TIMEDELTA_ARG=timedelta(days=1))
            self.assertEqual(cfg.INT_ARG, 10)
            self.assertFalse(cfg.BOOL_ARG)

    def test_config(self):
        cfg = Config(
            INT_ARG=2,
            INT_ARG_2=10,
            STR_ARG='1234ABCD',
            LIST_ARG=list('12345678'),
            SUB_CONFIG={'ARG_1': 1, 'ARG_2': 'ABCD'},
            SUB_CONFIGS=[{'ARG_1': 2, 'ARG_2': 'EFGH'}, {'ARG_1': 3, 'ARG_2': 'IJKL'}])
        self.assertEqual(cfg.INT_ARG, 2)
        self.assertEqual(cfg.SUB_CONFIG.ARG_1, 1)

    def test_sample(self):
        cfg = Config()
        expected = {'INT_ARG': 1,
                    'INT_ARG_2': 0,
                    'LIST_ARG': ['a', 'b', 'c', 'd'],
                    'STR_ARG': 'abcd',
                    'SUB_CONFIG': {'ARG_1': 10, 'ARG_2': 'abc'},
                    'SUB_CONFIGS': [{'ARG_1': 10, 'ARG_2': 'abc'}]}
        self.assertDictEqual(expected, cfg.sample_dict())

    def test_load_from_env(self):
        os.environ.update({
            'TEST_ALPHA': 'ALPHA',
            'TESTING_BETA': 'BETA',
            'TEST_GAMMA': '1'
        })
        cfg = EnvConfig.load_from_env()
        self.assertEqual('ALPHA', cfg.TESTING_ALPHA)
        self.assertEqual('BETA', cfg.TESTING_BETA)
        self.assertTrue(cfg.TESTING_GAMMA)

    def test_load_from_file(self):
        with tempfile.NamedTemporaryFile('w', delete=True) as tmp:
            tmp.write(
                '{"TEST_ALPHA": "ALPHA", "TESTING_BETA": "BETA", "TEST_GAMMA": true}')
            tmp.flush()
            cfg = EnvConfig.load_from_file(tmp.name)
        self.assertEqual('ALPHA', cfg.TESTING_ALPHA)
        self.assertEqual('BETA', cfg.TESTING_BETA)
        self.assertTrue(cfg.TESTING_GAMMA)
