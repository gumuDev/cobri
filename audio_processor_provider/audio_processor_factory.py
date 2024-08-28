from .audio_processor_telegram import AudioProcessorTelegram
from .audio_processor_whatsapp import AudioProcessorWhatsapp

class AudioProcessorFactory:
    
    def __init__(self):
        self.audio_processor = {
            'TELEGRAM': AudioProcessorTelegram,
            'WHATSAPP': AudioProcessorWhatsapp
        }
    
    def get_audio_processor(self, provider):
        audio_processor_class = self.audio_processor.get(provider)
        if audio_processor_class:
            return audio_processor_class()
        raise ValueError(f"Unrecognized provider type: {provider}")