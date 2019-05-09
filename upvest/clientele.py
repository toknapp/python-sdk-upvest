import json

from upvest.config import API_VERSION
from upvest.model import Assets, Wallets, Transactions
from upvest.authentication import OAuth

class UpvestClienteleAPI(object):
    def __init__(self, client_id, client_secret, username, password, base_url='https://api-playground.eu.upvest.co/'):
        # Create request instance providing access credentials
        self.auth_instance = OAuth(client_id=client_id, client_secret=client_secret, username=username, password=password, base_url=base_url)
        self.assets = Assets(self.auth_instance)
        self.wallets = Wallets(self.auth_instance)
