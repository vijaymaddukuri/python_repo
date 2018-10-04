import unittest
from backupjob.rabbitmq import RabbitMq
from backupjob.tests.mocked_rabbitmq import rabbitmqmockmethods
from mock import patch
def mock_get_config(key, attribute):
    data_dict = {"rabbitmq": {"RABBIT_MQ_IP": "localhost",
                              "RABBIT_MQ_USERNAME": "mqadmin",
                              "RABBIT_MQ_PASSWORD": "mqadminpassword"}}
    return data_dict[key][attribute]

class TestRabbitmq(unittest.TestCase):

    @patch('backupjob.rabbitmq.pika.BlockingConnection')
    @patch('backupjob.rabbitmq.get_config')
    def test_publish_message(self, config_mock, blocking_connection_mock):
        blocking_connection_mock.return_value = rabbitmqmockmethods()
        config_mock.side_effect = mock_get_config
        rmq = RabbitMq()
        result = rmq.publish_message({"key1": "value1"})
        self.assertEqual(result, None)
