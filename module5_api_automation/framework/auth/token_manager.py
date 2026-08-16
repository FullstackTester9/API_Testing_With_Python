# =====================================================
# The job of "TokenManager" is to store token, retrieve
# token, check whether token exists and remove token.
# =====================================================

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