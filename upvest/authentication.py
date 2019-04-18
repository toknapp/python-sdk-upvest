import time
import json
import hmac
import hashlib
import requests

from upvest.config import ENCODING
from upvest.config import OAUTH_PATH
from upvest.config import API_VERSION
from upvest.config import BASE_URL
from upvest.config import GRANT_TYPE
from upvest.config import SCOPE

class KeyAuth(object):
    def __init__(self, api_key=None, api_secret=None, api_passphrase=None, **kwargs):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_passphrase = api_passphrase

    def get_headers(self, method=None, path=None, body=None, **kwargs):
        body = json.dumps(body) if body else None
        timestamp = str(int(time.time()))
        # Compose the message as a concatenation of all info we are sending along with the request
        message = timestamp + method + API_VERSION + path + (body or '')
        # Generate signature, in order to prevent manipulation of payload in flight
        signature = hmac.new(str.encode(self.api_secret),
                             msg=message.encode(ENCODING),
                             digestmod=hashlib.sha512).hexdigest()
        # Generate message headers
        headers = {
            'Content-Type': 'application/json',
            'X-UP-API-Key': self.api_key,
            'X-UP-API-Signature': signature,
            'X-UP-API-Timestamp': timestamp,
            'X-UP-API-Passphrase': self.api_passphrase,
            'X-UP-API-Signed-Path': API_VERSION + path,
        }
        return headers

class OAuth(object):
    def __init__(self, client_id=None, client_secret=None, username=None, password=None, **kwargs):
        self.path = API_VERSION + OAUTH_PATH
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password

    def get_headers(self, **req_params):
        # Set header content-type to x-www-form-urlencoded
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        body = {
            'grant_type': GRANT_TYPE,
            'scope': SCOPE,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'username': self.username,
            'password': self.password,
        }
        # send x-www-form-urlencoded payload to clientele API.
        r = requests.post(BASE_URL+self.path, data=body, headers=headers)
        # Retrieve and return OAuth token
        oauth_token = r.json()['access_token']
        headers = {
            'Authorization': f'Bearer {oauth_token}',
            'Content-Type': 'application/json',
        }
        return headers
