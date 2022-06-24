import unittest
import tempfile

from gs.dotenv import load_env


class TestDotEnv(unittest.TestCase):

    def test_just_extra_source(self):

        with self.assertLogs('gs.dotenv', level='INFO') as cm:
            self.assertTrue(
                load_env(extra_source={'TEST_DOTENV': 'test'}, verbose=True))
            self.assertEqual(
                cm.output, ['INFO:gs.dotenv:load_env(extra_source={\'TEST_DOTENV\': \'test\'})'])

    def test_envfile(self):
        with tempfile.NamedTemporaryFile('w', prefix='.env', delete=True) as tmp:
            tmp.write('TEST_DOTENV=test\n# comment\nTEST_DOTENV2=test2=test3\n')
            tmp.flush()
            with self.assertLogs('gs.dotenv', level='INFO') as cm:
                self.assertTrue(
                    load_env(file_name=tmp.name, verbose=True))
                self.assertEqual(
                    cm.output, [f"INFO:gs.dotenv:load_env(file_name={tmp.name}) - {{'TEST_DOTENV': 'test', 'TEST_DOTENV2': 'test2=test3'}}"])

    def test_unexistent_file(self):
        self.assertFalse(load_env(file_name='/tmp/nonexistent.env'))
