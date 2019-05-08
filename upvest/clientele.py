import json

from upvest.config import API_VERSION
from upvest.config import BASE_URL 
from upvest.model import Assets, Wallets, Transactions
from upvest.authentication import OAuth

class UpvestClienteleAPI(object):
    def __init__(self, client_id, client_secret, username, password):
        # Create request instance providing access credentials
        self.auth_instance = OAuth(client_id=client_id, client_secret=client_secret, username=username, password=password)
        self.assets = Assets(self.auth_instance)
        self.wallets = Wallets(self.auth_instance)