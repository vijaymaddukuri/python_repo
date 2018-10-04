import unittest

from os import path
from ONBFactory.config.common import Common
from common import functions


class TestYaml(unittest.TestCase):
    def setUp(self):
        self.configPath_postive = path.normpath(path.join(Common.SITE_ROOT,
                                                          "common", "tests/test_resources/text.yaml"))
        self.configPath_negative = "tests/test_resourcess/text.yaml"
        self.data = {'a list': [1, 42, 3.141, 1337, 'help'],
                     'another_dict': {'foo': 'bar',
                                      'key': 'value',
                                      'the answer': 42}}

    def test_utils_yaml_positive(self):
        # Write YAML file
        functions.dict_to_yaml(self.data, self.configPath_postive)
        self.assertEqual(functions.get_config('another_dict', 'foo', self.configPath_postive), 'bar')

    def test_utils_yaml_negative(self):
        # # Write YAML file
        with self.assertRaises(Exception) as context:
            functions.dict_to_yaml(self.data, self.configPath_negative)
            self.assertTrue('No such file' in str(context.exception))


class TestGetPg(unittest.TestCase):
    """
    To test the proper return of Protection Group when Proper retention Policy details are entered
    """
    def test_get_pg_for_retention_time_valid(self):
        pg = functions.get_pg_for_retention_time(15, 'Day')
        self.assertEqual(pg, "Bronze-Filesystem15")

    def test_get_pg_for_retention_time_invalid_type(self):
        pg = functions.get_pg_for_retention_time(15, 'Daysssss')
        self.assertEqual(pg, "Invalid type")

    def test_get_pg_for_retention_time_PG_doesnt_exist(self):
        pg = functions.get_pg_for_retention_time(999999, 'Day')
        self.assertEqual(pg, "")


if __name__ == '__main__':
    unittest.main()
