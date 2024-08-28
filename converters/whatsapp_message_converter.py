from .message_converter import MessageConverter
from models.message import Message
from models.text_message import TextMessage
from models.audio_message import AudioMessage


class WhatsappMessageConverter(MessageConverter):
    provider = "WHATSAPP"

    def convert_to_message(self, message: dict, phone_id) -> Message:

        if "text" in message.get("type"):
            message_text = message["text"]["body"]
            return TextMessage(phone_id, self.provider, message_text)
        if "audio" in message.get("type"):
            file_id = message["audio"]["id"]
            return AudioMessage(phone_id, self.provider, file_id)
        else:
            raise ValueError(f"Unsupported message type")
