from message_converter import MessageConverter

class TelegramMessageConverter(MessageConverter):

    def convert_to_message(self, message):
        return super().convert_to_message(message)