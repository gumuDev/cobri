from .telegram_audio_converter import TelegramAudioConverter

class AudioProcessorTelegram:
    
    def get_audio(self, file_id):
        telegram_auido = TelegramAudioConverter()
        telegram_auido.download_file(file_id)
        mp3 = telegram_auido.convert_to_mp3()
        return mp3