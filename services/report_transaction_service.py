from .transaction import Transaction
from utils.excel_generator import ExcelGenerator
from utils.s3uploader import S3Uploader
import os

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = 'us-east-1'

class ReportTransactionService(Transaction):

    def __init__(self, clientSupabase, message_response) -> None:
        self.clientSupabase = clientSupabase
        self.message_response = message_response

    def process_transaction(self, details, phone_id):
        if isinstance(details, list):
            for detail in details:
                self.execute_report(detail, phone_id)
        else:
            self.execute_report(detail, phone_id)
    
    def execute_report(self, filter, phone_id):
        response_report = self.clientSupabase.get_report_by_filter(filter, phone_id)
        if len(response_report) != 0:
             excel_generator = ExcelGenerator(response_report)
             excel_file = excel_generator.generate_excel(filter.get("transaction_type"))
             s3_uploader = S3Uploader(S3_BUCKET_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)
             file_name = f"reporte_{filter.get("transaction_type")}.xlsx"
             file_url = s3_uploader.upload_file(excel_file, file_name)
             message = f"Aqui esta tu reporte de {filter.get("transaction_type")} descargalo de aqui [descargar]({file_url})"
             self.send_message(message, phone_id)
        else:
            self.send_message(f"No tiene reporte de {filter.get("transaction_type")}", phone_id)

    def send_message(self, details, phone_id):
        message_generated = details
        self.message_response.send_message(message_generated, phone_id)
    
    def get_type(self):
        return 'report'
