from .text_message_processor import TextMessageProcessor
from .audio_message_processor import AudioMessageProcessor

class ProcessorFactory:
    @staticmethod
    def get_processor(processor_type):
        if 'text' in processor_type:
            return TextMessageProcessor()
        elif 'voice' in processor_type:
            return AudioMessageProcessor()
        elif 'audio' in processor_type:
            return AudioMessageProcessor()
        else:
            raise ValueError(f"Unknown processor type: {processor_type}")