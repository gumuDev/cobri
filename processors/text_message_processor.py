from .message_processor import MessageProcessor
from chat_gpt_api.processor_gpt_request import ProcessorGptRequest

class TextMessageProcessor(MessageProcessor):
    
    def process_message(self, message: dict, client):
        try:
         return ProcessorGptRequest.get_json_from_prompt(message.text, client)
        except Exception as ex:
         print(ex)