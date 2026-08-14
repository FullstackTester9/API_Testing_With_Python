class TokenManager:

    def __init__(self):
        self._token = None

    def set_token(self, token):
        self._token = token

    def get_token(self):
        return self._token

    def clear_token(self):
        self._token = None

    def has_token(self):
        return self._token is not None