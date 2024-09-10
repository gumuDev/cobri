class GptResponse:
    def __init__(self, request_message: str,
                 response_message: str):
        self.response_message = response_message
        self.request_message = request_message