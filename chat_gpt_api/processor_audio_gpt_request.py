from .processor_gpt_request import ProcessorGptRequest
import os
class ProcessorAudioGptRequest:

    @staticmethod
    def get_json_from_prompt(audio_file, client):
        transcription = client.audio.transcriptions.create(
                   model="whisper-1", 
                   file=audio_file,
                   response_format="text")
        
        os.remove(audio_file.name)
        print(f"Archivo OGG '{audio_file.name}' eliminado")

        response =  ProcessorGptRequest.get_json_from_prompt(transcription, client)
        return response