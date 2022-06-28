"""Configuration tests"""
import math
from typing import List
import unittest

from datetime import datetime, date, timedelta

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


class ConfigTypes(BaseConfig):
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
