import json

from upvest.config import API_VERSION
from upvest.config import BASE_URL 
from upvest.utils import Request
from upvest.authentication import OAuth

class UpvestClienteleAPI(object):
    def __init__(self, client_id, client_secret, username, password):
        # Create request instance providing access credentials
        self.auth_instance = OAuth(client_id=client_id, client_secret=client_secret, username=username, password=password)
        
    # def _tx_speed_to_fee(self, speed, asset_id):
    #     path = '/price/'
    #     r = Request().get(auth_instance=self.auth_instance, path=path + asset_id)
    #     return json.loads(r)['speed']

    def list_assets(self):
        path = '/assets/'
        return Request().get(auth_instance=self.auth_instance, path=path)

    def list_wallets(self): 
        # Retrieve list of all wallets for a user
        path = '/kms/wallets/'
        return Request().get(auth_instance=self.auth_instance, path=path)


    def list_wallet(self, wallet_id):
        # Retrieve specific wallet for a user
        path = f'/kms/wallets/{wallet_id}'
        return Request().get(auth_instance=self.auth_instance, path=path)

    def create_wallet(self, asset_id):
        # Get desired asset id from assets list
        path = '/kms/wallets/'
        # Provide password and asset_id for wallet creation
        body = {
            'password' : self.auth_instance.password,
            'asset_id' : asset_id,
        }
        return Request().post(auth_instance=self.auth_instance, path=path, body=body)   

    def send_transaction(self, wallet_id, asset_id, quantity, fee, recipient):
        # Define tx endpoint
        path = '/tx/'

        # fee = self._tx_speed_to_fee(speed, asset_id)
        # Provide password and asset_id for wallet creation
        body = {
            'password' : self.auth_instance.password,
            'wallet_id': wallet_id,
            'asset_id' : asset_id,
            'quantity' : quantity,
            'fee': fee,
            'recipient' : recipient,
        }
        response = Request().post(auth_instance=self.auth_instance, path=path, body=body)
        print(response.text)
        return response

    def list_transaction(self, txhash):
        # Define tx endpoint
        path = '/tx/'
        return Request().post(auth_instance=self.auth_instance, path=path + txhash)
