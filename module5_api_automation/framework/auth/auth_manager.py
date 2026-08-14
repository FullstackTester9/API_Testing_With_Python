from framework.auth.token_manager import TokenManager


class AuthenticationManager:

    def __init__(
        self,
        api_client,
        config,
        token_manager
    ):
        self.api_client = api_client
        self.config = config
        self.token_manager = token_manager

    def login(self):

        auth_config = self.config["authentication"]

        payload = {
            "username": auth_config["username"],
            "password": auth_config["password"]
        }

        response = self.api_client.post(
            auth_config["login_endpoint"],
            json=payload
        )

        if response.status_code not in [200, 201]:
            raise RuntimeError(
                f"Authentication failed. "
                f"Status code: {response.status_code}"
            )

        response_data = response.json()

        token = response_data.get("token")

        if not token:
            raise RuntimeError(
                "Authentication succeeded but token was not returned."
            )

        self.token_manager.set_token(token)

        return token

    def get_token(self):
        return self.token_manager.get_token()

    def clear_token(self):
        self.token_manager.clear_token()