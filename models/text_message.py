from .message import Message

class TextMessage(Message):
    def __init__(self, id_client: str, provider: str, text: str):
        super().__init__(type="text", id_client=id_client, provider=provider)
        self.text = text