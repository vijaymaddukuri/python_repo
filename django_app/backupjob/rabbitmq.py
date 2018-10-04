import pika
import json
import logging
from backupjob.messagebroker import MessageBroker
from common.constants import EXCHANGE_NAME
from common.constants import ROUTING_KEY
from common.constants import QUEUE_NAME
from common.constants import RABBITMQ_KEY
from common.functions import get_config

logger = logging.getLogger(__name__)

class RabbitMq(MessageBroker):
    """
    Rabbitmq abstract class
    """
    def __init__(self):
        """
        :param:
        :return:
        """
        self.broker = get_config(RABBITMQ_KEY, "RABBIT_MQ_IP")
        self.user = get_config(RABBITMQ_KEY, "RABBIT_MQ_USERNAME")
        self.password = get_config(RABBITMQ_KEY, "RABBIT_MQ_PASSWORD")
        self.__get_connection_channel()
        self.channel.exchange_declare(exchange=EXCHANGE_NAME,
                                      exchange_type="topic")
        self.__disconnect_connection()

    def __get_connection_channel(self):
        credentials = pika.PlainCredentials(self.user, self.password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.broker,
                                                                            credentials=credentials))
        self.channel = self.connection.channel()

    def __bind_exchange(self):
        """
        Bind the exchange and queue.
        """
        self.channel.queue_declare(queue=QUEUE_NAME, durable=True)
        self.channel.queue_bind(exchange=EXCHANGE_NAME,
                                queue=QUEUE_NAME,
                                routing_key=ROUTING_KEY)

    def __disconnect_connection(self):
        """
        Disconnect connection.
        """
        self.connection.close()

    def publish_message(self, message):
        """
        publish message to the queue.
        :param message: message.
        :return:
        """
        logger.info("Publishing message to the queue")
        self.__get_connection_channel()
        self.__bind_exchange()
        self.channel.queue_declare(queue=QUEUE_NAME, durable=True)
        message_str = json.dumps(message)
        self.channel.basic_publish(exchange=EXCHANGE_NAME,
                                   routing_key=ROUTING_KEY,
                                   body=message_str,
                                   properties=pika.BasicProperties(
                                       delivery_mode=2,
                                   ))
        logger.debug("Message sent {}".format(message_str))
        self.__disconnect_connection()
