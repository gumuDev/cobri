from .message import Message

class AudioMessage(Message):
    def __init__(self, id_client: str, provider: str, file_id: str):
        super().__init__(type="audio", id_client=id_client, provider=provider)
        self.file_id = file_id