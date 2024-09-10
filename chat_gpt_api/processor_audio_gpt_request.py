from .processor_analize_request import ProcessorAnalizeRequest
import os
class ProcessorAudioGptRequest:

    @staticmethod
    def get_json_from_prompt(audio_file, client):
        transcription = client.audio.transcriptions.create(
                   model="whisper-1", 
                   file=audio_file,
                   response_format="text")
        
        os.remove(audio_file.name)

        response =  ProcessorAnalizeRequest.get_json_analize_from_prompt(transcription, client)
        return response