from .purchase_transaction_service import PurchaseTransactionService
from .sell_transaction_service import SellTransactionService
from .report_transaction_service import ReportTransactionService

class TransactionService:

    def __init__(self, client_supabase, message_response):
        self.client_supabase = client_supabase
        self.message_response = message_response
        self.transaction_services = {
            'purchase': PurchaseTransactionService,
            'sell': SellTransactionService,
            'report': ReportTransactionService
        }

    def getTransactionType(self, transaction_type):
        service_class = self.transaction_services.get(transaction_type)
        if service_class:
            return service_class(self.client_supabase, self.message_response)
        raise ValueError(f"Unrecognized transaction type: {transaction_type}")