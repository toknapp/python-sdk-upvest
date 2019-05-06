from upvest.utils import Request
from upvest.utils import PaginatedResponse

# Endpoint related objects
class UserInstance(object):
    def __init__(self, auth_instance, username):
        self.path = '/tenancy/users/'
        self.auth_instance = auth_instance
        self.username = username

    def update(self, current_password, new_password):
        # Provide current and new password
        body = {
            'old_password': current_password,
            'new_password': new_password,
        }
        return Request().patch(auth_instance=self.auth_instance, path=self.path + self.username, body=body)

    def delete(self):
        # Deregister a user
        return Request().delete(auth_instance=self.auth_instance, path=self.path + self.username)


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
        return Request().post(auth_instance=self.auth_instance, path=self.path, body=body)

    def get(self, username):
        response = Request().get(auth_instance=self.auth_instance, path=self.path + username)
        username = response.data['username']
        return UserInstance(self.auth_instance, username)

    def all(self):
        # Retrieve user list
        return Request().get(auth_instance=self.auth_instance, path=self.path, response_instance=PaginatedResponse)


class Assets(object):
    def __init__(self, auth_instance):
        self.path = '/assets/'
        self.auth_instance = auth_instance

    def all(self):
        return Request().get(auth_instance=self.auth_instance, path=self.path, response_instance=PaginatedResponse)


class Wallets(object):
    def __init__(self, auth_instance):
        self.path = '/kms/wallets/'
        self.auth_instance = auth_instance

    def create(self, asset_id):
        # Get desired asset id from assets list
        # Provide password and asset_id for wallet creation
        body = {
            'password': self.auth_instance.password,
            'asset_id': asset_id,
        }
        return Request().post(auth_instance=self.auth_instance, path=self.path, body=body)

    def get(self, wallet_id):
        # Retrieve specific wallet for a user
        return Request().get(auth_instance=self.auth_instance, path=self.path + wallet_id)

    def all(self):
        # Retrieve list of all wallets for a user
        return Request().get(auth_instance=self.auth_instance, path=self.path, response_instance=PaginatedResponse)


class Transactions(object):
    def __init__(self, auth_instance):
        self.path = '/tx/'
        self.auth_instance = auth_instance

    def send(self, wallet_id, asset_id, quantity, fee, recipient):
        # Provide password and asset_id for wallet creation
        body = {
            'password': self.auth_instance.password,
            'wallet_id': wallet_id,
            'asset_id': asset_id,
            'quantity': quantity,
            'fee': fee,
            'recipient': recipient,
        }
        response = Request().post(auth_instance=self.auth_instance, path=self.path, body=body)
        return response

    def get(self, txhash):
        # Define tx endpoint
        return Request().post(auth_instance=self.auth_instance, path=self.path + txhash)
