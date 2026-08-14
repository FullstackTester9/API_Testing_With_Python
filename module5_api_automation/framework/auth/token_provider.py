class TokenProvider:

    def __init__(self, token_manager):
        self.token_manager = token_manager

    def get_token(self):
        return self.token_manager.get_token()