from abc import ABC, abstractmethod

class MessageConverter(ABC):
    
    @abstractmethod
    def convert_to_message(self, message):
        pass