import hashlib
import hmac
import json
import time
from urllib.parse import urljoin

import requests

from upvest.config import API_VERSION, ENCODING, GRANT_TYPE, OAUTH_PATH, SCOPE
from upvest.exceptions import InvalidRequest


class KeyAuth:
    def __init__(self, api_key=None, api_secret=None, api_passphrase=None, base_url=None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_passphrase = api_passphrase
        self.base_url = base_url

    def get_headers(self, method=None, path=None, body=None):
        body = json.dumps(body) if body else None
        timestamp = str(int(time.time()))
        # Compose the message as a concatenation of all info we are sending along with the request
        message = timestamp + method + API_VERSION + path + (body or "")
        # Generate signature, in order to prevent manipulation of payload in flight
        signature = hmac.new(
            str.encode(self.api_secret), msg=message.encode(ENCODING), digestmod=hashlib.sha512
        ).hexdigest()
        # Generate message headers
        headers = {
            "Content-Type": "application/json",
            "X-UP-API-Key": self.api_key,
            "X-UP-API-Signature": signature,
            "X-UP-API-Timestamp": timestamp,
            "X-UP-API-Passphrase": self.api_passphrase,
            "X-UP-API-Signed-Path": API_VERSION + path,
        }
        return headers


class OAuth:
    def __init__(self, client_id=None, client_secret=None, username=None, password=None, base_url=None):
        self.path = API_VERSION + OAUTH_PATH
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.base_url = base_url

    def get_headers(self):
        # Set header content-type to x-www-form-urlencoded
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        body = {
            "grant_type": GRANT_TYPE,
            "scope": SCOPE,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": self.username,
            "password": self.password,
        }

        # send x-www-form-urlencoded payload to clientele API.
        req = requests.post(urljoin(self.base_url, self.path), data=body, headers=headers)
        if req.status_code >= 300:
            raise InvalidRequest(req.text)

        # Retrieve and return OAuth token
        oauth_token = req.json()["access_token"]
        headers = {"Authorization": f"Bearer {oauth_token}", "Content-Type": "application/json"}
        return headers
