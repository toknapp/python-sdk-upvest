import hashlib
import hmac
import time
from urllib.parse import urljoin
from upvest.__pkginfo__ import DEFAULT_USERAGENT

import requests

from upvest.config import API_VERSION, ENCODING, GRANT_TYPE, OAUTH_PATH, SCOPE
from upvest.exceptions import InvalidRequest


class KeyAuth:
    """
    ### API Keys Authentication
    The Upvest API uses the notion of _tenants_, which represent customers that build their platform upon the Upvest API. The end-users of the tenant (i.e. your customers), are referred to as _clients_. A tenant is able to manage their users directly (CRUD operations for the user instance) and is also able to initiate actions on the user's behalf (create wallets, send transactions).

    The authentication via API keys and secret allows you to perform all tenant related operations.
    Please create an API key pair within the [Upvest account management](https://login.upvest.co/).

    The default `BASE_URL` for both authentication objects is `https://api.playground.upvest.co`, but feel free to adjust it, once you retrieve your live keys.
    Next, create an `UpvestTenancyAPI` object in order to authenticate your API calls:
    ```python
    from upvest.tenancy import UpvestTenancyAPI
    tenancy = UpvestTenancyAPI(API_KEY, API_SECRET, API_PASSPHRASE, base_url=BASE_URL) # or base_url=None to use the playground environment (default)
    ```
    """

    def __init__(self, api_key=None, api_secret=None, api_passphrase=None, base_url=None, user_agent=None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_passphrase = api_passphrase
        self.base_url = base_url
        self.user_agent = user_agent or DEFAULT_USERAGENT

    def get_headers(self, method, path, body=None):
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
    """
    ### OAuth Authentication
    The authentication via OAuth allows you to perform operations on behalf of your user.
    For more information on the OAuth concept, please refer to our [documentation](https://doc.upvest.co/docs/oauth2-authentication).
    Again, please retrieve your client credentials from the [Upvest account management](https://login.upvest.co/).

    Next, create an `UpvestClienteleAPI` object with these credentials and your user authentication data in order to authenticate your API calls on behalf of a user:
    ```python
    from upvest.clientele import UpvestClienteleAPI
    clientele = UpvestClienteleAPI(CLIENT_ID, CLIENT_SECRET, username, password, base_url=BASE_URL) # or base_url=None to use the playground environment (default)
    ```
    """

    def __init__(
        self, client_id=None, client_secret=None, username=None, password=None, base_url=None, user_agent=None
    ):
        self.path = API_VERSION + OAUTH_PATH
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.base_url = base_url
        self.user_agent = user_agent or DEFAULT_USERAGENT

        self.access_token = None
        self.access_token_expiry = None

    def get_token(self):
        # allow for some clock drift
        if self.access_token and time.time() < self.access_token_expiry - 3600:
            return self.access_token

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
        response = requests.post(urljoin(self.base_url, self.path), data=body, headers=headers)
        if response.status_code >= 300:
            raise InvalidRequest(response)

        # Retrieve and return OAuth token
        resp_json = response.json()
        self.access_token = resp_json["access_token"]
        self.access_token_expiry = time.time() + resp_json["expires_in"]
        return self.access_token

    def get_headers(self, **_):
        return {"Authorization": f"Bearer {self.get_token()}", "Content-Type": "application/json"}
