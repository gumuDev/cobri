from .message_processor import MessageProcessor
from models.audio_message import AudioMessage
from audio_processor_provider.audio_processor_factory import AudioProcessorFactory
from chat_gpt_api.processor_audio_gpt_request import ProcessorAudioGptRequest

class AudioMessageProcessor(MessageProcessor):
    
    def process_message(self, message: AudioMessage, client):
        try:
            audio_factory = AudioProcessorFactory()
            audio_processor = audio_factory.get_audio_processor(message.provider)
            mp3_file = audio_processor.get_audio(message.file_id)
            audio_file= open(mp3_file, "rb")
            return ProcessorAudioGptRequest.get_json_from_prompt(audio_file, client)
        except Exception as ex:
            print(ex)