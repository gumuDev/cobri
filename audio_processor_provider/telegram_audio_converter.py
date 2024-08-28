import requests
import subprocess
import uuid
import os

class TelegramAudioConverter:
    _instance = None
    bot_token = os.getenv("BOT_TOKEN_TELEGRAM")

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TelegramAudioConverter, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return  # Ya inicializado
        if self.bot_token is not None:
            self.bot_token = self.bot_token
            self.download_url = f"https://api.telegram.org/bot{self.bot_token}/getFile?file_id="
        else:
            raise ValueError("bot_token must be provided on the first initialization")
        self._initialized = True

        # Crear el folder 'audio' si no existe
        self.audio_folder = "audio"
        os.makedirs(self.audio_folder, exist_ok=True)

    def _generate_filename(self, extension):
        """Genera un nombre de archivo aleatorio con la extensión dada."""
        return f"{uuid.uuid4().hex}.{extension}"

    def download_file(self, file_id):
        response = requests.get(self.download_url + file_id)
        file_info = response.json()
        file_path = file_info['result']['file_path']
        file_url = f"https://api.telegram.org/file/bot{self.bot_token}/{file_path}"
        
        # Generar un nombre aleatorio para el archivo OGG
        ogg_filename = os.path.join(self.audio_folder, self._generate_filename("ogg"))
        
        # Descargar el archivo
        response = requests.get(file_url)
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
        os.remove(self.ogg_filename)
        print(f"Archivo OGG '{self.ogg_filename}' eliminado")
        
        return mp3_filename  # Devuelve el nombre del archivo MP3

    def get_mp3_content(self, mp3_filename):
        with open(mp3_filename, "rb") as file:
            return file.read()
