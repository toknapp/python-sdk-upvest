from upvest.config import API_VERSION
from upvest.config import BASE_URL
from upvest.authentication import KeyAuth
from upvest.utils import Request, User, Users

class UpvestTenancyAPI(object):
    def __init__(self, api_key, api_secret, api_passphrase):
        # Create request instance providing access credentials
        self.auth_instance = KeyAuth(api_key=api_key, api_secret=api_secret, api_passphrase=api_passphrase)
        self.users = Users(self.auth_instance)
