from typing import List
import unittest

from gs.config.class_properties import get_fields_default_values, get_types, get_comments, get_envs


class DummyClass(object):
    """Dummy class
    for testing
    purposes"""

    INT_FIELD = 1  # INT FIELD TEXT
    FLOAT_FIELD: float = 0.2  # FLOAT FIELD COMMENT
    STR_LIST_FIELD: List[str]  # ENV:STR_LIST_FIELD_ENV

    def __init__(self):
        self.STR_FIELD = 'abc'  # STR FIELD COMMENT


class TestClassProperties(unittest.TestCase):

    def test_get_fields_defaults_values(self):
        defaults = get_fields_default_values(DummyClass)
        self.assertDictEqual(
            defaults, {'INT_FIELD': 1, 'FLOAT_FIELD': 0.2})

    def test_get_types(self):
        types = get_types(DummyClass)
        self.assertDictEqual(
            types, {'FLOAT_FIELD': (float, False),
                    'STR_LIST_FIELD': (str, True)})

    def test_get_comments(self):
        comments = get_comments(DummyClass)
        self.assertDictEqual(comments,
                             {'INT_FIELD': 'INT FIELD TEXT',
                              'FLOAT_FIELD': 'FLOAT FIELD COMMENT',
                              'STR_FIELD': 'STR FIELD COMMENT',
                              'STR_LIST_FIELD': 'ENV:STR_LIST_FIELD_ENV'})

    def test_get_envs(self):
        envs = get_envs(DummyClass)
        self.assertDictEqual(envs, {'STR_LIST_FIELD': 'STR_LIST_FIELD_ENV'})
