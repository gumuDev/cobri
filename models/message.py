class Message:
    def __init__(self, type: str, id_client: str,
                 provider: str):
        self.type = type
        self.id_client = id_client
        self.provider = provider