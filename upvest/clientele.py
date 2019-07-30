from upvest.authentication import OAuth
from upvest.config import UPVEST_API_TARGET
from upvest.model import Assets, Wallets


class UpvestClienteleAPI:
    def __init__(self, client_id, client_secret, username, password, base_url=None):
        base_url = base_url or UPVEST_API_TARGET
        self.auth_instance = OAuth(
            client_id=client_id, client_secret=client_secret, username=username, password=password, base_url=base_url
        )
        self.assets = Assets(self.auth_instance)
        self.wallets = Wallets(self.auth_instance)
