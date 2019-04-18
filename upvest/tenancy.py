from upvest.config import API_VERSION
from upvest.config import BASE_URL
from upvest.authentication import KeyAuth
from upvest.utils import Request

path = '/tenancy/users/'

class UpvestTenancyAPI(object):
    def __init__(self, api_key, api_secret, api_passphrase):
        # Create request instance providing access credentials
        self.auth_instance = KeyAuth(api_key=api_key, api_secret=api_secret, api_passphrase=api_passphrase)

    def register_user(self, username, password):
        # Set username and password for the user
        body = {
            'username' : username,
            'password' : password,
        }
        return Request().post(auth_instance=self.auth_instance, path=path, body=body)

    def list_user(self, username):
        # Retrieve single user      
        return Request().get(auth_instance=self.auth_instance, path=path + username)
    

    def list_users(self): 
        # Retrieve user list
        return Request().get(auth_instance=self.auth_instance, path=path)

    def change_password(self, username, current_password, new_password): 
        # Provide current and new password     
        body = {
            'old_password' : current_password,
            'new_password' : new_password,
        }
        return Request().patch(auth_instance=self.auth_instance, path=path + username, body=body)

    def deregister_user(self, username):  
        # Deregister a user
        return Request().delete(auth_instance=self.auth_instance, path=path + username)