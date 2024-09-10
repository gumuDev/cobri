from .message_converter import MessageConverter
from models.message import Message
from models.text_message import TextMessage
from models.audio_message import AudioMessage

class TelegramMessageConverter(MessageConverter):
    provider = 'TELEGRAM'

    def convert_to_message(self, message: dict, phone_id) -> Message:
        if 'text' in message.get('message'):
            message_text =  message["message"]['text']
            return TextMessage(phone_id, self.provider, message_text)
        if 'voice' in message.get('message'):
            file_id = message['message']['voice']['file_id']
            return AudioMessage(phone_id, self.provider, file_id)
        else:
            raise ValueError(f"No soportamos esto tipo de mensajes solo audio y texto")