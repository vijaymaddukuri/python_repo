import unittest
import saltmanager.salt_utils as salt
import requests
from mock import patch
from common.constants import SALT_MASTER_ERROR
from common.exceptions import SALTException

def mock_raise_exception_get_fqdn():
    raise Exception("Unknown exception")

def mock_get_config_data(key, attribute):
    data_dict = {"salt_retries_config_values": {"SALT_PING_NO_OF_RETRIES": 1,
                                                "SALT_PING_RETRIES_TIMEOUT":1},
                 "salt_master_details":
                                             {"MASTER_IP": "1.2.3.4",
                                              "MASTER_API_PORT": "8000",
                                              "MASTER_API_USERNAME": "master_user",
                                              "MASTER_API_PASSWORD": "master_pwd",
                                              "MASTER_SALT_BASE_LOCATION": "/etc/salt",
                                              "SSH_PORT_NUMBER": 22}
                }

    return data_dict[key][attribute]
                 
class TestSaltManager(unittest.TestCase):
    @patch("saltmanager.salt_utils.get_config")
    def test_init_saltmanager(self, yaml_mock):
        yaml_mock.return_value = "string"
        salt.SaltNetAPI()

    @patch("saltmanager.salt_utils.get_config")
    def test_url(self, yaml_mock):
        yaml_mock.return_value = "string"
        sa = salt.SaltNetAPI()
        result = sa.url("url")
        self.assertEqual(result, "http://string:string/url")

    @patch("saltmanager.salt_utils.get_config")
    @patch("saltmanager.salt_utils.requests.Session.post")
    def test_login(self, post_mock, yaml_mock):
        yaml_mock.return_value = "string"
        sa = salt.SaltNetAPI()
        post_mock.return_value = {"status": 200}
        result = sa.login()
        self.assertEqual(result, {"status": 200})
   
    @patch('saltmanager.salt_utils.get_config')
    def test_verify_login_handle_connection_error(self, mock_config_data):
        mock_config_data.return_value = mock_get_config_data
        sa = salt.SaltNetAPI()
        try:
            sa.verify_login(None)
        except SALTException as e:
            self.assertEqual(e.error_message, SALT_MASTER_ERROR['SALT001_CONNECTION_ERROR'])
            self.assertEqual(e.salt_resp, None)

    @patch('saltmanager.salt_utils.get_config')
    @patch("saltmanager.salt_utils.SaltNetAPI.login")
    def test_verify_login_handle_login_error(self, login_mock, mock_config_data):
        mock_config_data.return_value = mock_get_config_data
        sa = salt.SaltNetAPI()
        login_mock.return_value.ok = False
        try:
            sa.verify_login(login_mock)
        except SALTException as e:
            self.assertEqual(e.error_message, SALT_MASTER_ERROR['SALT002_LOGIN_ERROR'])

    @patch("saltmanager.salt_utils.get_config")
    @patch("saltmanager.salt_utils.requests.Session.post")
    @patch("saltmanager.salt_utils.SaltNetAPI.login")
    def test_vm_minion_status_positive(self, login_mock, post_mock, yaml_mock):
        yaml_mock.return_value = "string"
        login_mock.return_value.ok = True
        sa = salt.SaltNetAPI()
        sa.salt_session = requests.session()
        post_mock.return_value.json.return_value = {'return': [{'minion_name': True}]}
        result = sa.get_vm_minion_status('1.1.1.1', 'ipcidr')
        self.assertEqual(result['status'], True)

    @patch("saltmanager.salt_utils.get_config")
    @patch("saltmanager.salt_utils.requests.Session.post")
    @patch("saltmanager.salt_utils.SaltNetAPI.login")
    def test_vm_minion_status_handle_salt_connection_error(self, login_mock, post_mock, yaml_mock):
        yaml_mock.return_value = "string"
        login_mock.return_value = None
        sa = salt.SaltNetAPI()
        sa.salt_session = requests.session()
        result = sa.get_vm_minion_status('1.1.1.1', 'ipcidr')
        expected = {'status': False,
                    'comment': SALT_MASTER_ERROR['SALT001_CONNECTION_ERROR']}
        self.assertEqual(result, expected)

    @patch("saltmanager.salt_utils.get_config")
    @patch("saltmanager.salt_utils.requests.Session.post")
    @patch("saltmanager.salt_utils.SaltNetAPI.login")
    def test_vm_minion_status_handle_login_falied(self, login_mock, post_mock, yaml_mock):
        yaml_mock.return_value = "string"
        login_mock.return_value.ok = False
        sa = salt.SaltNetAPI()
        sa.salt_session = requests.session()
        result = sa.get_vm_minion_status('1.1.1.1', 'ipcidr')
        expected = {'status': False,
                    'comment': SALT_MASTER_ERROR['SALT002_LOGIN_ERROR']}
        self.assertEqual(result, expected)

    @patch("saltmanager.salt_utils.get_config")
    @patch("saltmanager.salt_utils.requests.Session.post")
    @patch("saltmanager.salt_utils.SaltNetAPI.login")
    def test_vm_minion_status_hanlde_null_response(self, login_mock, post_mock, yaml_mock):
        yaml_mock.return_value = "string"
        login_mock.return_value.ok = True
        sa = salt.SaltNetAPI()
        sa.salt_session = requests.session()
        post_mock.return_value.json.return_value = {}
        result = sa.get_vm_minion_status('1.1.1.1', 'ipcidr')
        expected = {'status': False,
                    'comment': SALT_MASTER_ERROR['SALT003_EMPTY_MINION_RESPONSE']}
        self.assertEqual(result, expected)

    @patch("saltmanager.salt_utils.get_config")
    @patch("saltmanager.salt_utils.requests.Session.post")
    @patch("saltmanager.salt_utils.SaltNetAPI.login")
    def test_vm_minion_status_hanlde_minion_not_responding(self, login_mock, post_mock, yaml_mock):
        yaml_mock.return_value = "string"
        login_mock.return_value.ok = True
        sa = salt.SaltNetAPI()
        sa.salt_session = requests.session()
        post_mock.return_value.json.return_value = {'return': [{'minion_name': False}]}
        result = sa.get_vm_minion_status('1.1.1.1', 'ipcidr')
        expected = {'status': False,
                    'comment': SALT_MASTER_ERROR['SALT004_MINION_NOT_RESPONDING']}
        self.assertEqual(result, expected)

    @patch("saltmanager.salt_utils.get_config")
    @patch("saltmanager.salt_utils.requests.Session.post")
    @patch("saltmanager.salt_utils.SaltNetAPI.login")
    def test_get_minion_name_positive(self, login_mock, post_mock, yaml_mock):
        yaml_mock.return_value = "string"
        login_mock.return_value.ok = True
        sa = salt.SaltNetAPI()
        sa.salt_session = requests.session()
        post_mock.return_value.json.return_value = {"return": [{"minion_name": "minion_name"}]}
        result = sa.get_minion_name('1.1.1.1', 'ipcidr')
        expected = {'status': True,
                    'minion_name': 'minion_name'}
        self.assertEqual(expected['status'], result['status'])
        self.assertEqual(expected['minion_name'], result['minion_name'])

    @patch("saltmanager.salt_utils.get_config")
    @patch("saltmanager.salt_utils.requests.Session.post")
    @patch("saltmanager.salt_utils.SaltNetAPI.login")
    def test_get_minion_name_handle_salt_connection_error(self, login_mock, post_mock, yaml_mock):
        yaml_mock.return_value = "string"
        login_mock.return_value = None
        sa = salt.SaltNetAPI()
        sa.salt_session = requests.session()
        result = sa.get_minion_name('1.1.1.1', 'ipcidr')
        expected = {'status': False,
                    'comment': SALT_MASTER_ERROR['SALT001_CONNECTION_ERROR']}
        self.assertEqual(expected, result)

    @patch("saltmanager.salt_utils.get_config")
    @patch("saltmanager.salt_utils.requests.Session.post")
    @patch("saltmanager.salt_utils.SaltNetAPI.login")
    def test_get_minion_name_handle_login_error(self, login_mock, post_mock, yaml_mock):
        yaml_mock.return_value = "string"
        login_mock.return_value.ok = False
        sa = salt.SaltNetAPI()
        sa.salt_session = requests.session()
        result = sa.get_minion_name('1.1.1.1', 'ipcidr')
        expected = {'status': False,
                    'comment': SALT_MASTER_ERROR['SALT002_LOGIN_ERROR']}
        self.assertEqual(expected, result)

    @patch("saltmanager.salt_utils.get_config")
    @patch("saltmanager.salt_utils.requests.Session.post")
    @patch("saltmanager.salt_utils.SaltNetAPI.login")
    def test_get_minion_name_handle_null_response(self, login_mock, post_mock, yaml_mock):
        yaml_mock.return_value = "string"
        login_mock.return_value.ok = True
        sa = salt.SaltNetAPI()
        sa.salt_session = requests.session()
        post_mock.return_value.json.return_value = {}
        result = sa.get_minion_name('1.1.1.1', 'ipcidr')
        expected = {'status': False,
                    'comment': SALT_MASTER_ERROR['SALT003_EMPTY_MINION_RESPONSE']}
        self.assertEqual(expected, result)

    @patch("saltmanager.salt_utils.get_config")
    @patch("saltmanager.salt_utils.requests.Session.post")
    @patch("saltmanager.salt_utils.SaltNetAPI.login")
    def test_get_minion_name_handle_minion_not_responding(self, login_mock, post_mock, yaml_mock):
        yaml_mock.return_value = "string"
        login_mock.return_value.ok = True
        sa = salt.SaltNetAPI()
        sa.salt_session = requests.session()
        post_mock.return_value.json.return_value = {'return': [{'minion_name': ['minion did not return']}]}
        result = sa.get_minion_name('1.1.1.1', 'ipcidr')
        expected = {'status': False,
                    'comment': SALT_MASTER_ERROR['SALT004_MINION_NOT_RESPONDING']}
        self.assertEqual(expected, result)

    @patch("saltmanager.salt_utils.get_config")
    @patch("saltmanager.salt_utils.requests.Session.post")
    @patch("saltmanager.salt_utils.SaltNetAPI.login")
    def test_send_grains_and_sync_positive(self, login_mock, post_mock, yaml_mock):
        yaml_mock.return_value = "string"
        login_mock.return_value.ok = True
        sa = salt.SaltNetAPI()
        sa.salt_session = requests.session()
        post_mock.return_value.json.return_value = {"return": [{"minion_name": "minion_name"}]}
        result = sa.send_grains_and_sync('1.1.1.1')
        self.assertEqual(result['status'], True)

    @patch("saltmanager.salt_utils.get_config")
    @patch("saltmanager.salt_utils.requests.Session.post")
    @patch("saltmanager.salt_utils.SaltNetAPI.login")
    def test_send_grains_and_sync_negative(self, login_mock, post_mock, yaml_mock):
        yaml_mock.return_value = "string"
        login_mock.return_value.ok = True
        sa = salt.SaltNetAPI()
        sa.salt_session = requests.session()
        post_mock.return_value.json.return_value = {"return": [{"minion_name": "minion_Name"}]}
        post_mock.return_value.json.return_value = {}
        result = sa.send_grains_and_sync('1.1.1.1')
        self.assertEqual(result['status'], False)

    @patch("saltmanager.salt_utils.get_config")
    @patch("saltmanager.salt_utils.requests.Session.post")
    @patch("saltmanager.salt_utils.SaltNetAPI.login")
    def test_check_master_minion_connection_positive(self, login_mock, post_mock, yaml_mock):
        yaml_mock.return_value = "string"
        login_mock.return_value.ok = True
        sa = salt.SaltNetAPI()
        sa.salt_session = requests.session()
        post_mock.return_value.json.return_value = {'return': [{"dummy.xstest.local": True}]}
        result = sa.check_master_minion_connection('dummy.xstest.local')
        self.assertEqual(result['status'], True)

    @patch("saltmanager.salt_utils.get_config")
    @patch("saltmanager.salt_utils.requests.Session.post")
    @patch("saltmanager.salt_utils.SaltNetAPI.login")
    def test_check_master_minion_connection_negative(self, login_mock, post_mock, yaml_mock):
        yaml_mock.return_value = "string"
        login_mock.return_value.ok = True
        sa = salt.SaltNetAPI()
        sa.salt_session = requests.session()
        post_mock.return_value.json.return_value = {}
        result = sa.check_master_minion_connection('dummy.xstest.local')
        self.assertEqual(result['status'], False)

    @patch("saltmanager.salt_utils.get_config")
    @patch("saltmanager.salt_utils.requests.Session.post")
    @patch("saltmanager.salt_utils.SaltNetAPI.login")
    def test_get_fqdn_from_minion_id_handle_login_failed(self, login_mock, post_mock, yaml_mock):
        yaml_mock.return_value = "string"
        login_mock.return_value.ok = False
        sa = salt.SaltNetAPI()
        sa.salt_session = requests.session()
        post_mock.return_value.json.return_value = {}
        result = sa.get_fqdn_from_minion_id('dummy.xstest.local')
        message = 'Unable to establish connection with the salt master machine. ' \
                  'Please ensure the machine is up and Salt Master/Salt NetApi services are running.'
        self.assertEqual(result['status'], False)
        self.assertEqual(result['comment'], message)

    @patch("saltmanager.salt_utils.get_config")
    @patch("saltmanager.salt_utils.requests.Session.post")
    @patch("saltmanager.salt_utils.SaltNetAPI.login")
    def test_get_fqdn_from_minion_id_handle_null_response_object(self, login_mock, post_mock, yaml_mock):
        yaml_mock.return_value = "string"
        login_mock.return_value.ok = True
        sa = salt.SaltNetAPI()
        sa.salt_session = requests.session()
        post_mock.return_value.json.return_value = {}
        result = sa.get_fqdn_from_minion_id('dummy.xstest.local')
        message = "Response is not in proper format."
        self.assertEqual(result['status'], False)
        self.assertEqual(result['comment'], message)

    @patch("saltmanager.salt_utils.get_config")
    @patch("saltmanager.salt_utils.requests.Session.post")
    @patch("saltmanager.salt_utils.SaltNetAPI.login")
    def test_get_fqdn_from_minion_id_handle_empty_response_from_minion(
            self, login_mock, post_mock, yaml_mock):
        # Test Post method return empty object
        yaml_mock.return_value = "string"
        login_mock.return_value.ok = True
        sa = salt.SaltNetAPI()
        sa.salt_session = requests.session()
        post_mock.return_value.json.return_value = {'return': []}
        result = sa.get_fqdn_from_minion_id('dummy.xstest.local')
        message = "Response is not in proper format."
        self.assertEqual(result['status'], False)
        self.assertEqual(result['comment'], message)

    @patch("saltmanager.salt_utils.get_config")
    @patch("saltmanager.salt_utils.requests.Session.post")
    @patch("saltmanager.salt_utils.SaltNetAPI.login")
    def test_get_fqdn_from_minion_id_handle_response_when_fqdn_not_set(
            self, login_mock, post_mock, yaml_mock):
        # Test Post method return no fqdn
        yaml_mock.return_value = "string"
        login_mock.return_value.ok = True
        sa = salt.SaltNetAPI()
        sa.salt_session = requests.session()
        post_mock.return_value.json.return_value = {'return': [{'dummy.xstest.local': {}}]}
        result = sa.get_fqdn_from_minion_id('dummy.xstest.local')
        message = "Unable to fetch the FQDN, response return object is empty"
        self.assertEqual(result['status'], False)
        self.assertEqual(result['comment'], message)

    @patch("saltmanager.salt_utils.get_config")
    @patch("saltmanager.salt_utils.requests.Session.post")
    @patch("saltmanager.salt_utils.SaltNetAPI.login")
    def test_get_fqdn_from_minion_id_handle_runtime_exception(self, login_mock, post_mock, yaml_mock):
        yaml_mock.return_value = "string"
        login_mock.return_value.ok = True
        sa = salt.SaltNetAPI()
        sa.salt_session = requests.session()
        with self.assertRaises(Exception) as context:
            post_mock.side_effect = mock_raise_exception_get_fqdn
            sa.get_fqdn_from_minion_id('dummy.xstest.local')
            self.assertTrue('Unknown exception' in str(context.exception))

    @patch("saltmanager.salt_utils.get_config")
    @patch("saltmanager.salt_utils.requests.Session.post")
    @patch("saltmanager.salt_utils.SaltNetAPI.login")
    def test_get_fqdn_from_minion_id_positive(self, login_mock, post_mock, yaml_mock):
        yaml_mock.return_value = "string"
        login_mock.return_value.ok = True
        sa = salt.SaltNetAPI()
        sa.salt_session = requests.session()
        post_mock.return_value.json.return_value = \
            {'return': [{'dummy.xstest.local': {'fqdn': 'dummy.xstest.local'}}]}
        result = sa.get_fqdn_from_minion_id('dummy.xstest.local')
        self.assertEqual(result['status'], True)
        self.assertEqual(result['fqdn'], 'dummy.xstest.local')
   
    @patch('saltmanager.salt_utils.get_config')
    @patch('saltmanager.salt_utils.SaltNetAPI.get_vm_minion_status')
    def test_check_minion_status_success(self, mock_minion_api, mock_config_api):
        mock_config_api.side_effect = mock_get_config_data
        mock_minion_api.return_value = {'status':True}
        saltapi = salt.SaltNetAPI()
        result = saltapi.check_minion_status("1.1.1.1")
        self.assertTrue(result, True)

    @patch('saltmanager.salt_utils.get_config')
    @patch('saltmanager.salt_utils.SaltNetAPI.get_vm_minion_status')
    def test_check_minion_status_fail(self, mock_minion_api, mock_config_api):
        mock_config_api.side_effect = mock_get_config_data
        mock_minion_api.return_value = {'status':False}
        saltapi = salt.SaltNetAPI()
        result = saltapi.check_minion_status("1.1.1.1")
        self.assertFalse(result, False)

    @patch('saltmanager.salt_utils.get_config')
    @patch('saltmanager.salt_utils.SaltNetAPI.get_minion_name')
    def test_get_minion_name_from_ip_success(self, mock_minion_api, mock_config_api):
        mock_config_api.side_effect = mock_get_config_data
        mock_minion_api.return_value = {'status':True, 'minion_name': 'minion1'}
        saltapi = salt.SaltNetAPI()
        result = saltapi.get_minion_name_from_ip("1.1.1.1")
        self.assertTrue(result, True)

    @patch('saltmanager.salt_utils.get_config')
    @patch('saltmanager.salt_utils.SaltNetAPI.get_minion_name')
    def test_get_minion_name_from_ip_failure(self, mock_minion_api, mock_config_api):
        mock_config_api.side_effect = mock_get_config_data
        mock_minion_api.return_value = False
        saltapi = salt.SaltNetAPI()
        result = saltapi.get_minion_name_from_ip("1.1.1.1")
        self.assertFalse(result, False)


if __name__ == '__main__':
    unittest.main()
