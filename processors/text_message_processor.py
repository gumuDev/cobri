from .message_processor import MessageProcessor
from chat_gpt_api.processor_analize_request import ProcessorAnalizeRequest

class TextMessageProcessor(MessageProcessor):
    
    def process_message(self, message: dict, client):
        try:
         return ProcessorAnalizeRequest.get_json_analize_from_prompt(message.text, client)
        except Exception as ex:
         print(ex)