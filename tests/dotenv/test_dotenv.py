"""Test dotenv module"""
import os
import unittest
import tempfile

from gs.dotenv import load_env


class TestDotEnv(unittest.TestCase):
    """Test dotenv"""

    def test_just_extra_source(self):
        """Validates extra_source argument"""

        with self.assertLogs('gs.dotenv', level='INFO') as logs:
            self.assertTrue(
                load_env(extra_source={'TEST_DOTENV': 'test'}, verbose=True))
            self.assertEqual(
                logs.output, ['INFO:gs.dotenv:load_env(extra_source={\'TEST_DOTENV\': \'test\'})'])

    def test_envfile(self):
        """Validates envfile argument"""
        with tempfile.NamedTemporaryFile('w', prefix='.env', delete=True) as tmp:
            tmp.write('TEST_DOTENV=test\n# comment\nTEST_DOTENV2=test2=test3\n')
            tmp.flush()

            self.assertTrue(load_env(file_name=tmp.name))
            self.assertEqual('test', os.environ['TEST_DOTENV'])
            self.assertEqual('test2=test3', os.environ['TEST_DOTENV2'])

    def test_unexistent_file(self):
        """Validates nonexistent file"""
        self.assertFalse(load_env(file_name='/tmp/nonexistent.env'))
