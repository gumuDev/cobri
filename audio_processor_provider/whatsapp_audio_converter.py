import os
import requests
import subprocess
import uuid

class WhatsappAudioConverter:
    wa_token = os.getenv("WHATSAPP_TOKEN")

    def __init__(self) -> None:
        self.download_url = f"https://graph.facebook.com/v17.0/"
        self.audio_folder = "audio"
        os.makedirs(self.audio_folder, exist_ok=True)

    def download_file(self, file_id):
        headers = {"Authorization": f"Bearer {self.wa_token}"}
        url = self.download_url + file_id
        response_wa = requests.get(url, headers=headers)
        file_info = response_wa.json()
        audio_url = file_info['url']
        
        headers = {
            "Authorization": f"Bearer {self.wa_token}",
            "Content-Type": "application/json",
        }

        response = requests.get(audio_url, headers=headers)
        # Generar un nombre aleatorio para el archivo OGG
        ogg_filename = os.path.join(self.audio_folder, self._generate_filename("ogg"))
        with open(ogg_filename, "wb") as file:
            file.write(response.content)
        print(f"Archivo descargado como '{ogg_filename}'")
        self.ogg_filename = ogg_filename  # Guardar el nombre del archivo OGG para uso posterior
    
    def convert_to_mp3(self):
        # Generar un nombre aleatorio para el archivo MP3
        mp3_filename = os.path.join(self.audio_folder, self._generate_filename("mp3"))
        
        # Convertir el archivo OGG a MP3
        subprocess.run(["ffmpeg", "-i", self.ogg_filename, mp3_filename], check=True)
        print(f"Archivo convertido a '{mp3_filename}'")
        
        # Eliminar el archivo OGG después de la conversión
        # os.remove(self.ogg_filename)
        # print(f"Archivo OGG '{self.ogg_filename}' eliminado")
        
        return mp3_filename  # Devuelve el nombre del archivo MP3

    def get_mp3_content(self, mp3_filename):
        with open(mp3_filename, "rb") as file:
            return file.read()
        
    def _generate_filename(self, extension):
        """Genera un nombre de archivo aleatorio con la extensión dada."""
        return f"{uuid.uuid4().hex}.{extension}"
    