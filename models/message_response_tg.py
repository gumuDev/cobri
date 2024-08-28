from .message_response import MessageResponse

class MessageResponseTG(MessageResponse):
    def __init__(self, message, client_id, mode):
        super().__init__(message, client_id)
        self.mode = mode