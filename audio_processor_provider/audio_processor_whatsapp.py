from .whatsapp_audio_converter import WhatsappAudioConverter

class AudioProcessorWhatsapp:

    def get_audio(self, file_id):
        whatsapp_auido = WhatsappAudioConverter()
        whatsapp_auido.download_file(file_id)
        mp3 = whatsapp_auido.convert_to_mp3()
        return mp3
