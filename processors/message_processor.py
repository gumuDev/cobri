from abc import ABC, abstractmethod

class MessageProcessor(ABC):
    @abstractmethod
    def process_message(self, message, client):
        pass
