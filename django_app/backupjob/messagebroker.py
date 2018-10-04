from abc import ABC, abstractmethod

class MessageBroker(ABC):
    """abstract class for publish message"""
    @abstractmethod
    def publish_message(self, message):
        pass
