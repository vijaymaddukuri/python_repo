import unittest
from mock import patch
from os import path
from ONBFactory.config.common import Common
from common import functions

networker_dict = {
           "password": "",
           "pg15": "Bronze-Filesystem15",
           "pg30": "Bronze-Filesystem30",
           "url": "",
           "username": ""
       }

def mock_get_config(key, attribute):
    data_dict = {"networker_server_details": {"NETWORKER_URL": "https://10.100.249.48:9090",
                                              "NETWORKER_USERNAME": "administrator",
                                              "NETWORKER_PASSWORD": "Password1!",
                                              "NETWORKER_PG_15": "Bronze-Filesystem15",
                                              "NETWORKER_PG_30": "Bronze-Filesystem30",
                                             }
                }
    return data_dict[key][attribute]

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
    @patch('common.functions.get_config')
    def test_get_pg_for_retention_time_valid(self, config_mock):
        config_mock.side_effect = mock_get_config 
        pg = functions.get_pg_for_retention_time(networker_dict, 15, 'Day')
        self.assertEqual(pg, "Bronze-Filesystem15")

    @patch('common.functions.get_config')
    def test_get_pg_for_retention_time_invalid_type(self, config_mock):
        config_mock.side_effect = mock_get_config 
        pg = functions.get_pg_for_retention_time(networker_dict, 15, 'Daysssss')
        self.assertEqual(pg, "Invalid type")

    @patch('common.functions.get_config')
    def test_get_pg_for_retention_time_PG_doesnt_exist(self, config_mock):
        config_mock.side_effect = mock_get_config 
        pg = functions.get_pg_for_retention_time(networker_dict, 999999, 'Day')
        self.assertEqual(pg, "")


if __name__ == '__main__':
    unittest.main()
