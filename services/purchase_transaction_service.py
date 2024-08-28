from .transaction import Transaction
from datetime import datetime


class PurchaseTransactionService(Transaction):
    def __init__(self, clientSupabase, message_response) -> None:
        self.clientSupabase = clientSupabase
        self.message_response = message_response

    def process_transaction(self, details, phone_id):
        purchase_current = []
        for purchase in details:
                current_date = datetime.now()
                current_date_str = current_date.strftime("%Y-%m-%d %H:%M:%S")
                data = {
                    "item": purchase["item"],
                    "price": purchase["price"],
                    "phone": phone_id,
                    "created_at": current_date_str,
                    "quantity": purchase["quantity"],
                }
                purchase_current.append(data)

        self.clientSupabase.save_purchase(purchase_current)
        self.send_message(details, phone_id)
        
    def send_message(self, details, phone_id):
        message_generated = self.message_response.generate_message(details, self.get_type())
        self.message_response.send_message(message_generated, phone_id)

    
    def get_type(self):
        return "purchase"
