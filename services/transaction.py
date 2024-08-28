from abc import ABC, abstractmethod

class Transaction(ABC):
    @abstractmethod
    def process_transaction(self, details, phone_id):
        pass

    @abstractmethod
    def get_type():
        pass

    @abstractmethod
    def send_message(self, details, phone_id):
        pass