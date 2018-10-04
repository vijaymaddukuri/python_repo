import unittest
from mock import patch
from django.test import Client
from backupjob.tests.mocked_rabbitmq import rabbitmqmockmethods
from common.constants import API_URLS


def mock_get_config(key, attribute):
    data_dict = {"rabbitmq": {"RABBIT_MQ_IP": "localhost",
                              "RABBIT_MQ_USERNAME": "mqadmin",
                              "RABBIT_MQ_PASSWORD": "mqadminpassword"}}
    return data_dict[key][attribute]


class TestBackUp(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    @patch('backupjob.rabbitmq.pika.BlockingConnection')
    @patch('backupjob.rabbitmq.RabbitMq.publish_message')
    @patch('backupjob.views.logger.exception')
    @patch('backupjob.rabbitmq.get_config')
    @patch('common.functions.get_config', return_value="correct")
    def test_auth_exception(self, credential_mock, config_mock, exception_mock,
                            publish_message_mock, blocking_connection_mock):
        blocking_connection_mock.return_value = rabbitmqmockmethods()
        config_mock.side_effect = mock_get_config

        # Valid request.
        url = API_URLS["SERVICE_BASE_URL"] + '/backup/enable/'
        req_data = {
            "RetentionDays": 72,
            "Callback": "example.com",
            "VirtualMachineID": "8E87A82F-D40C-4200-A62E-A8E12291B0BD",
            "TenantID": "8E87A82F-D40C-4200-A62E-A8E12291B0BD",
            "VirtualMachineHostName": "SHWETAGARG071018B"}
        publish_message_mock.side_effect = KeyError
        exception_mock.return_value = None
        with self.assertRaises(Exception):
            with self.assertRaises(AttributeError):
                response = self.client.post(url, req_data)
                self.assertEqual(response.status_code, 500)

    @patch('backupjob.rabbitmq.pika.BlockingConnection')
    @patch('backupjob.rabbitmq.RabbitMq.publish_message')
    @patch('backupjob.views.logger.exception')
    @patch('backupjob.rabbitmq.get_config')
    @patch('common.functions.get_config', return_value="correct")
    def test_missing_authorization_header(self, cred_mock, config_mock, exception_mock,
                                          publish_message_mock, blocking_connection_mock):
        blocking_connection_mock.return_value = rabbitmqmockmethods()
        config_mock.side_effect = mock_get_config
        url = API_URLS["SERVICE_BASE_URL"] + '/backup/enable/'
        req_data = {
            "RetentionDays": 72,
            "Callback": "example.com",
            "VirtualMachineID": "8E87A82F-D40C-4200-A62E-A8E12291B0BD",
            "TenantID": "8E87A82F-D40C-4200-A62E-A8E12291B0BD",
            "VirtualMachineHostName": "SHWETAGARG071018B"}
        publish_message_mock.return_value = None
        response = self.client.post(url, data=req_data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    @patch('backupjob.rabbitmq.pika.BlockingConnection')
    @patch('backupjob.rabbitmq.RabbitMq.publish_message')
    @patch('backupjob.views.logger.exception')
    @patch('backupjob.rabbitmq.get_config')
    @patch('common.functions.get_config', return_value="correct")
    def test_invalid_authorization_header(self, cred_mock, config_mock, exception_mock,
                                          publish_message_mock, blocking_connection_mock):
        blocking_connection_mock.return_value = rabbitmqmockmethods()
        config_mock.side_effect = mock_get_config
        url = API_URLS["SERVICE_BASE_URL"] + '/backup/enable/'
        req_data = {
            "RetentionDays": 72,
            "Callback": "example.com",
            "VirtualMachineID": "8E87A82F-D40C-4200-A62E-A8E12291B0BD",
            "TenantID": "8E87A82F-D40C-4200-A62E-A8E12291B0BD",
            "VirtualMachineHostName": "SHWETAGARG071018B"}
        publish_message_mock.return_value = None
        response = self.client.post(url, data=req_data, content_type="application/json",
                                    HTTP_AUTHORIZATION="Basic")
        self.assertEqual(response.status_code, 400)

    @patch('backupjob.rabbitmq.pika.BlockingConnection')
    @patch('backupjob.rabbitmq.RabbitMq.publish_message')
    @patch('backupjob.views.logger.exception')
    @patch('backupjob.rabbitmq.get_config')
    @patch('common.functions.get_config', return_value="correct")
    def test_unsupported_authorization_header(self, cred_mock, config_mock, exception_mock,
                                              publish_message_mock, blocking_connection_mock):
        blocking_connection_mock.return_value = rabbitmqmockmethods()
        config_mock.side_effect = mock_get_config
        url = API_URLS["SERVICE_BASE_URL"] + '/backup/enable/'
        req_data = {
            "RetentionDays": 72,
            "Callback": "example.com",
            "VirtualMachineID": "8E87A82F-D40C-4200-A62E-A8E12291B0BD",
            "TenantID": "8E87A82F-D40C-4200-A62E-A8E12291B0BD",
            "VirtualMachineHostName": "SHWETAGARG071018B"}
        publish_message_mock.return_value = None
        response = self.client.post(url, data=req_data, content_type="application/json",
                                    HTTP_AUTHORIZATION="Token Auth")
        self.assertEqual(response.status_code, 401)

    @patch('backupjob.rabbitmq.pika.BlockingConnection')
    @patch('backupjob.rabbitmq.RabbitMq.publish_message')
    @patch('backupjob.views.logger.exception')
    @patch('backupjob.rabbitmq.get_config')
    @patch('common.functions.get_config', return_value="correct")
    def test_wrong_credentials(self, credential_mock, config_mock, exception_mock,
                               publish_message_mock, blocking_connection_mock):
        blocking_connection_mock.return_value = rabbitmqmockmethods()
        config_mock.side_effect = mock_get_config
        url = API_URLS["SERVICE_BASE_URL"] + '/backup/enable/'
        req_data = {
            "RetentionDays": 72,
            "Callback": "example.com",
            "VirtualMachineID": "8E87A82F-D40C-4200-A62E-A8E12291B0BD",
            "TenantID": "8E87A82F-D40C-4200-A62E-A8E12291B0BD",
            "VirtualMachineHostName": "SHWETAGARG071018B"}
        publish_message_mock.return_value = None

        # Base64 encoded string "invalid_username:invalid_password"
        response = self.client.post(url, data=req_data, content_type="application/json",
                                    HTTP_AUTHORIZATION="Basic aW52YWxpZF91c2VybmFtZTppbnZhbGlkX3Bhc3N3b3Jk")
        self.assertEqual(response.status_code, 401)

