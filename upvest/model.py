from urllib.parse import urlsplit, urlunsplit, urlencode, parse_qs
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
        print(response.data)
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
        MAX_PAGE_SIZE = 100
        array_of_users = []
        path = f'/tenancy/users/?page_size={MAX_PAGE_SIZE}'
        listed_count = 0

        while listed_count < count:
            response = Response(Request().get(auth_instance=self.auth_instance, path=path))
            for user in response.data:
                username = user['username']
                array_of_users.append(UserInstance(self.auth_instance, username))
                listed_count += 1 
                if listed_count >= count:
                    break
            if response.raw.json()['next']:
                page_size = min(MAX_PAGE_SIZE, count - listed_count)
                path = response.raw.json()['next'].split(API_VERSION)[-1]
                path_parts = list(urlsplit(path))
                query = parse_qs(path_parts[3])
                query['page_size'] = [page_size]
                path_parts[3] = urlencode(query, doseq=True)
                path = urlunsplit(path_parts)
            else:
                break
        return array_of_users

    def all(self):
        MAX_PAGE_SIZE = 100
        array_of_users = []
        path = '/tenancy/users/?{MAX_PAGE_SIZE}'

        while True:
            response = Response(Request().get(auth_instance=self.auth_instance, path=path))
            for user in response.data:
                username = user['username']
                array_of_users.append(UserInstance(self.auth_instance, username))
            if response.raw.json()['next']:
                path = response.raw.json()['next'].split(API_VERSION)[-1]
                path_parts = list(urlsplit(path))
                query = parse_qs(path_parts[3])
                query['page_size'] = [MAX_PAGE_SIZE]
                path_parts[3] = urlencode(query, doseq=True)
                path = urlunsplit(path_parts)
            else:
                break
        return array_of_users

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
        MAX_PAGE_SIZE = 100
        array_of_assets = []
        path = '/assets/?{MAX_PAGE_SIZE}'

        while True:
            response = Response(Request().get(auth_instance=self.auth_instance, path=path))
            for asset in response.data:
                array_of_assets.append(AssetInstance(**asset))
            if response.raw.json()['next']:
                path = response.raw.json()['next'].split(API_VERSION)[-1]
                path_parts = list(urlsplit(path))
                query = parse_qs(path_parts[3])
                query['page_size'] = [MAX_PAGE_SIZE]
                path_parts[3] = urlencode(query, doseq=True)
                path = urlunsplit(path_parts)
            else:
                break
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
    
    def list(self, count):
        # Retrieve subset of wallets
        MAX_PAGE_SIZE = 100
        array_of_wallets = []
        path = f'/kms/wallets/?page_size={MAX_PAGE_SIZE}'
        listed_count = 0

        while listed_count < count:
            response = Response(Request().get(auth_instance=self.auth_instance, path=path))
            for wallet in response.data:
                array_of_wallets.append(WalletInstance(self.auth_instance, **wallet))
                listed_count += 1
                if listed_count >= count:
                    break
            if response.raw.json()['next']:
                page_size = min(MAX_PAGE_SIZE, count - listed_count)
                path = response.raw.json()['next'].split(API_VERSION)[-1]
                path_parts = list(urlsplit(path))
                query = parse_qs(path_parts[3])
                query['page_size'] = [page_size]
                path_parts[3] = urlencode(query, doseq=True)
                path = urlunsplit(path_parts)
            else:
                break
        return array_of_wallets
    
    def all(self):
        # Retrieve subset of wallets
        MAX_PAGE_SIZE = 100
        array_of_wallets = []
        path = f'/kms/wallets/?page_size={MAX_PAGE_SIZE}'

        while True:
            response = Response(Request().get(auth_instance=self.auth_instance, path=path))
            for wallet in response.data:
                array_of_wallets.append(WalletInstance(self.auth_instance, **wallet))
            if response.raw.json()['next']:
                path = response.raw.json()['next'].split(API_VERSION)[-1]
                path_parts = list(urlsplit(path))
                query = parse_qs(path_parts[3])
                query['page_size'] = [MAX_PAGE_SIZE]
                path_parts[3] = urlencode(query, doseq=True)
                path = urlunsplit(path_parts)
            else:
                break
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

    def list(self, count):
        # Retrieve subset of wallets
        MAX_PAGE_SIZE = 100
        array_of_transactions = []
        path = f'{self.path}{self.wallet_id}/transactions/?page_size={MAX_PAGE_SIZE}'
        listed_count = 0

        while listed_count < count:
            response = Response(Request().get(auth_instance=self.auth_instance, path=path))
            for transaction in response.data:
                array_of_transactions.append(TransactionInstance(**transaction))
                listed_count += 1
                if listed_count >= count:
                    break
            if response.raw.json()['next']:
                page_size = min(MAX_PAGE_SIZE, count - listed_count)
                path = response.raw.json()['next'].split(API_VERSION)[-1]
                path_parts = list(urlsplit(path))
                query = parse_qs(path_parts[3])
                query['page_size'] = [page_size]
                path_parts[3] = urlencode(query, doseq=True)
                path = urlunsplit(path_parts)
            else:
                break
        return array_of_transactions

    def all(self):
        MAX_PAGE_SIZE = 100
        array_of_transactions = []
        path = f'{self.path}{self.wallet_id}/transactions/?page_size={MAX_PAGE_SIZE}'

        while True:
            response = Response(Request().get(auth_instance=self.auth_instance, path=path))
            for transaction in response.data:
                array_of_transactions.append(TransactionInstance(**transaction))
            if response.raw.json()['next']:
                path = response.raw.json()['next'].split(API_VERSION)[-1]
                path_parts = list(urlsplit(path))
                query = parse_qs(path_parts[3])
                query['page_size'] = [MAX_PAGE_SIZE]
                path_parts[3] = urlencode(query, doseq=True)
                path = urlunsplit(path_parts)
            else:
                break
        return array_of_transactions