class MessageHandlerService():
    """Abstraction layer that will invoke the right broker method"""

    def __init__(self, msg_broker_instance):
        self.instance = msg_broker_instance

    def handle_message(self, message):
        return self.instance.publish_message(message)
