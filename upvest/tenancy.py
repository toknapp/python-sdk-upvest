from upvest.authentication import KeyAuth
from upvest.config import UPVEST_API_TARGET
from upvest.model import Assets, Users


class UpvestTenancyAPI:
    def __init__(self, api_key, api_secret, api_passphrase, base_url=None, user_agent=None):
        base_url = base_url or UPVEST_API_TARGET
        self.auth_instance = KeyAuth(
            api_key=api_key,
            api_secret=api_secret,
            api_passphrase=api_passphrase,
            base_url=base_url,
            user_agent=user_agent,
        )
        self.users = Users(self.auth_instance)
        self.assets = Assets(self.auth_instance)
