import time

from upvest.utils import Request, Response
from upvest.config import API_VERSION

# Endpoint related objects
class UserInstance(object):
    def __init__(self, auth_instance, username, recovery_kit=None):
        self.path = '/tenancy/users/'
        self.auth_instance = auth_instance
        self.username = username
        self.recovery_kit = recovery_kit

    def update(self, current_password, new_password):
        # Provide current and new password
        body = {
            'old_password': current_password,
            'new_password': new_password,
        }
        response = Response(Request().patch(auth_instance=self.auth_instance, path=self.path + self.username, body=body))
        username = response.data['username']
        return UserInstance(response, username)

    def delete(self):
        # Deregister a user
        return None


class Users(object):
    def __init__(self, auth_instance):
        self.path = '/tenancy/users/'
        self.auth_instance = auth_instance

    def create(self, username, password):
        # Set username and password for the user
        body = {
            'username': username,
            'password': password,
        }
        response = Response(Request().post(auth_instance=self.auth_instance, path=self.path, body=body))
        username = response.data['username']
        recovery_kit = response.data['recoverykit']
        return UserInstance(self.auth_instance, username, recovery_kit)

    def get(self, username):
        response = Response(Request().get(auth_instance=self.auth_instance, path=self.path + username))
        username = response.data['username']
        return UserInstance(self.auth_instance, username)

    def list(self, count):
        # Retrieve subset of users
        array_of_users = []
        self.path = '/tenancy/users/'
        if count <= 100:
            self.path = f'{self.path}?page_size={count}'
            response = Response(Request().get(auth_instance=self.auth_instance, path=self.path))
            for user in response.data:
                username = user['username']
                array_of_users.append(UserInstance(self.auth_instance, username))
            return len(array_of_users)
        else:
            i = 0
            remainder = count % 100
            iterations = ((count - remainder) / 100)
            self.path = f'/tenancy/users/?page_size=100'
            while i < iterations:
                response = Response(Request().get(auth_instance=self.auth_instance, path=self.path))
                for user in response.data:
                    username = user['username']
                    array_of_users.append(UserInstance(self.auth_instance, username))
                if response.raw.json()['next'] is None:
                    return len(array_of_users)
                else:
                    self.path = response.raw.json()['next'].split(API_VERSION)[-1]
                    i += 1
            if remainder == 0:
                return len(array_of_users)
            else:
                without_version = response.raw.json()['next'].split(API_VERSION)[-1]
                split_path = without_version.split('&page')[0]
                self.path = f'{split_path}&page_size={remainder}'
                response = Response(Request().get(auth_instance=self.auth_instance, path=self.path))
                for user in response.data:
                    username = user['username']
                    array_of_users.append(UserInstance(self.auth_instance, username))  
                return len(array_of_users)  
            
    def all(self):
        # Retrieve all users
        self.path = '/tenancy/users/?page_size=100'
        array_of_users = []
        while True:
            response = Response(Request().get(auth_instance=self.auth_instance, path=self.path))
            for user in response.data:
                username = user['username']
                array_of_users.append(UserInstance(self.auth_instance, username))
            if response.json()['next'] is None:
                return len(array_of_users)
            else:
                self.path = response.json()['next'].split(API_VERSION)[-1]

class AssetInstance(object):
    def __init__(self,**asset_attr):
        self.id = asset_attr['id']
        self.name = asset_attr['name']
        self.symbol = asset_attr['symbol']
        self.exponent = asset_attr['exponent']
        self.protocol = asset_attr['protocol']
        self.metadata = asset_attr['metadata']

class Assets(object):
    def __init__(self, auth_instance):
        self.path = '/assets/'
        self.auth_instance = auth_instance

    def all(self):
        response = Response(Request().get(auth_instance=self.auth_instance, path=self.path))
        array_of_assets = []
        for asset in response.data:
            array_of_assets.append(AssetInstance(**asset))
        while True:
            try:
                response = Response(Request().get(auth_instance=self.auth_instance, path=self.path))
                for asset in response.data:
                    array_of_assets.append(AssetInstance(**asset))
            except:
                return array_of_assets
        
class WalletInstance(object):
    def __init__(self, auth_instance, **wallet_attr):
        self.transactions = Transactions(auth_instance, wallet_attr['id'])
        self.id = wallet_attr['id']
        self.balances = wallet_attr['balances']
        self.protocol  = wallet_attr['protocol']
        self.address = wallet_attr['address']
        self.status = wallet_attr['status']

class Wallets(object):
    def __init__(self, auth_instance):
        self.path = '/kms/wallets/'
        self.auth_instance = auth_instance

    def create(self, asset_id, password):
        # Get desired asset id from assets list
        # Provide password and asset_id for wallet creation
        body = {
            'password': password,
            'asset_id': asset_id,
        }
        response = Response(Request().post(auth_instance=self.auth_instance, path=self.path, body=body))
        return WalletInstance(self.auth_instance, **response.data)

    def get(self, wallet_id):
        # Retrieve specific wallet for a user
        response = Response(Request().get(auth_instance=self.auth_instance, path=self.path + wallet_id))
        return WalletInstance(self.auth_instance, **response.data)
    
    def all(self):
        # Retrieve list of all wallets for a user
        response = Response(Request().get(auth_instance=self.auth_instance, path=self.path))
        array_of_wallets = []

        for wallet in response.data:
            array_of_wallets.append(WalletInstance(self.auth_instance, **wallet))
        while True:
            try:
                response = Response(Request().get(auth_instance=self.auth_instance, path=self.path))
                for wallet in response.data:
                    array_of_wallets.append(WalletInstance(self.auth_instance, **wallet))
            except:
                return array_of_wallets

class TransactionInstance(object):
    def __init__(self, **transaction_attr):
        self.path = '/kms/wallets/'
        self.txhash = transaction_attr['txhash']
        self.sender = transaction_attr['sender']
        self.recipient = transaction_attr['recipient']
        self.quantity = transaction_attr['quantity']
        self.fee = transaction_attr['fee']

class Transactions(object):
    def __init__(self, auth_instance, wallet_id):
        self.path = '/kms/wallets/'
        self.auth_instance = auth_instance
        self.wallet_id = wallet_id

    def create(self, password, asset_id, quantity, fee, recipient):
        # Provide password and asset_id for wallet creation
        body = {
            'password': password,
            'wallet_id': self.wallet_id,
            'asset_id': asset_id,
            'quantity': quantity,
            'fee': fee,
            'recipient': recipient,
        }
        response = Response(Request().post(auth_instance=self.auth_instance, path=f'{self.path}{self.wallet_id}/transactions/', body=body))    
        return TransactionInstance(**response.data)

    def get(self, txhash):
        # Define tx endpoint
        response = Response(Request().get(auth_instance=self.auth_instance, path=f'{self.path}{self.wallet_id}/transactions/{txhash}'))
        return TransactionInstance(**response.data)
  

