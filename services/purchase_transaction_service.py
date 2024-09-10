from .transaction import Transaction
from datetime import datetime
import logging


class PurchaseTransactionService(Transaction):
    def __init__(self, clientSupabase, message_response) -> None:
        self.clientSupabase = clientSupabase
        self.message_response = message_response

    def process_transaction(self, details, phone_id):
        try:
          purchase_current = []
          valid_items = list(filter(lambda item: all(key in item and item[key] not in [None, 'null', ''] for key in ['price', 'quantity', 'item']), details))
          invalid_items = list(filter(lambda item: not all(key in item and item[key] != 'null' for key in ['price', 'quantity', 'item']), details))
          
          for purchase in valid_items:
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
          self.send_message(valid_items, phone_id)
          if (len(invalid_items) != 0):
               self._send_message_invalid(invalid_items, phone_id)
        except Exception as ex:
             logging.exception("Failed to insert data", ex)
        
    def send_message(self, details, phone_id):
        message_generated = self.message_response.generate_message(details, self.get_type())
        self.message_response.send_message(message_generated, phone_id)

    def _send_message_invalid(self, details, phone_id):
        message_generated = self.message_response.generate_message_invalid(details, self.get_type())
        self.message_response.send_message(message_generated, phone_id)
         
    def get_type(self):
        return "purchase"
