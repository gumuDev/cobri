from models.message import Message
from processors.processor_factory import ProcessorFactory
from services.transaction_service import TransactionService


class MessageDispatcher:

    def __init__(self, message_response, sqs_client, client_supabase) -> None:
        self.message_response = message_response
        self.sqs_client = sqs_client
        self.client_supabase = client_supabase

    async def message_dispatch(self, message: Message, client):
        try:
           processor = ProcessorFactory.get_processor(message.type)
           response_from_chat_gpt = processor.process_message(message, client)
   
           if (response_from_chat_gpt is None or len(response_from_chat_gpt) == 0 
               or "message" in response_from_chat_gpt):
               
               self.message_response.send_message(
                   "No es una comprar o una venta", message.id_client
               )
               return
   
           self._process_message_response(response_from_chat_gpt, message)
        except Exception as ex:
            print(ex)
            self.message_response.send_message(
                   "Fallo al registrar por favor intentelo de nuevo", message.id_client
               )
            
    def _process_message_response(self, response: dict, message: Message):
        if "transactions" in response:
            transaction_map = {}
            # Llenar el diccionario con los detalles de cada tipo de transacción
            for transaction in response["transactions"]:
                try:
                   trans_type = transaction["type"]
                   transaction_service = TransactionService(
                       self.client_supabase, self.message_response
                   )
                   transaction = transaction_service.getTransactionType(trans_type)
   
                   details = self._get_details_by_type(response, trans_type)
   
                   # Si el tipo de transacción no existe en el diccionario, lo creamos
                   if trans_type not in transaction_map:
                       transaction_map[transaction] = []
   
                   # Añadir los detalles al tipo de transacción correspondiente
                   transaction_map[transaction].extend(details)

                except Exception as ex:
                   print(f'fallo {ex}')

            for transaction, details in transaction_map.items():
                trans_type = transaction.get_type()
                transaction.process_transaction(details, message.id_client)
                # message_generated = self.message_response.generate_message(
                #     details, trans_type
                # )
                # self.message_response.send_message(message_generated, message.id_client)

        elif "type" in response and "unknown" != response["type"]:
            trans_type = response["type"]
            transaction_service = TransactionService(
                self.client_supabase, self.message_response
            )

            transaction = transaction_service.getTransactionType(trans_type)
            details = response['details']
            if not isinstance(details, list):
                details = [response['details']]
            transaction.process_transaction(details, message.id_client)
            # transaction.send_message(details, message.id_client)

    def _get_details_by_type(self, data, type_filter):
        # Filtra las transacciones por tipo y extrae los detalles en una lista plana
        details = [
            transaction["details"]
            for transaction in data["transactions"]
            if transaction["type"] == type_filter
        ]
        flat_list = []

        for item in details:
            if isinstance(item, list):
                flat_list.extend(item)  # Añade los elementos de la lista anidada
            else:
                flat_list.append(item)

        return flat_list
