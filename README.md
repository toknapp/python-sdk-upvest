Installation
------
The Upvest SDK is available on PYPI. Install with pip:
```python
pip install upvest
```

Documentation
------
In order to retrieve your API credentials for using this Python client, you'll need to [sign up with Upvest](https://login.upvest.co/sign-up).

### API Keys Authentication
The authentication via API keys and secret allows you to perform all tenant related operations.
Create an API keypair within the dashboard.

Next, create an UpvestTenancyAPI object in order to authenticate your API calls:
```python
from upvest.tenancy import UpvestTenancyAPI
tenancy = UpvestTenancyAPI(API_KEY, API_SECRET, API_PASSPHRASE)
```

### OAuth Authentication
The authentication via OAuth allows you to perform operations on behalf of a user.
For more information on the OAuth concept, please refer to our [documentation](https://doc.upvest.co/docs/oauth2-authentication).
Retrieve your client credentials from the dashboard.

Next, create an UpvestClienteleAPI object in order to authenticate your API calls on behalf of a user:
```python
from upvest.clientele import UpvestClienteleAPI
clientele = UpvestClienteleAPI(CLIENT_ID, CLIENT_SECRET, username, password)
```

### API Calls
All tenancy related operations must be using the API Keys authentication, whereas all actions on a user's behalf need to be authenticated via OAuth. The API calls are built along those two authentication objects.

The methods allow for passing paramenters if needed. If required arguments are not provided, the respective error will be raised.

#### Response Object
All API calls return a ResponseObject. For your convenience we implemented two ways of reading data from this Object. Both the raw response, as well as the response data dict, are accessible via the ResponseObject's attributes.
Either you retrieve the actual API response object provided by the Upvest API:
```python
# Retrieve raw response obejct
clientele = UpvestClienteleAPI(CLIENT_ID, CLIENT_SECRET, username, password)
raw_response = clientele.list_wallets().raw
```
Or you decide to retrieve only the relevant data from the response as a python dict:
```python
# Retrieve response data
clientele = UpvestClienteleAPI(CLIENT_ID, CLIENT_SECRET, username, password)
data_response = clientele.list_wallets().data
```
The ResponseObject provides a convienient option for pagination. The Upvest API result arrays are limited to an item count of 10 per page, iteratable via the endpoints provided in the response with the ```next``` and ```previous``` keys. In order to use pagination with the Upvest Python library, simply write:
```python
# Previous Page
clientele = UpvestClienteleAPI(CLIENT_ID, CLIENT_SECRET, username, password)
response = clientele.list_wallets().previous()

# Next Page
clientele = UpvestClienteleAPI(CLIENT_ID, CLIENT_SECRET, username, password)
response = clientele.list_wallets().next()
```

Usage
------
### Tenancy
#### Create a user
```python
tenancy.register_user('username','password')
```
#### List a user
```python
tenancy.list_user('username')
```
#### List all users under tenancy
```python
tenancy.list_users()
```
#### Change password of a user
```python
tenancy.change_password('username', 'current_password', 'new_password')
```
#### Deregister a user
```python
tenancy.deregister_user('username')
```

### Clientele
#### List available assets
```python
clientele.list_assets()
```
#### Create a wallet for a user
```python
clientele.create_wallet('asset_id')
```
#### List all wallets for a user
```python
clientele.list_wallets()
```
#### List specific wallet for a user
```python
clientele.list_wallet('wallet_id')
```
#### Send transaction
```python
clientele.send_transaction('wallet_id', 'asset_id', 'quantity', 'fee', 'recipient')
```

Usage
------
## Tutorial
### Tenant Creation
The business "Successful blockchain project", founded by John Doe, would like to built a platform for Ethereum wallets with easy access and wallet management. Therefore, John visits the [Upvest Signup Page](https://login.upvest.co/sign-up), creates and account, and retrieves his API keys from the account management page. He is now able to create the API keys Authentication Object:
```python
# API Keys Object
from upvest.tenancy import UpvestTenancyAPI
tenancy = UpvestTenancyAPI(API_KEY, API_SECRET, API_PASSPHRASE)
```

### User Creation
John sets up his platform and soon has the first person signing up for his service. Jane Apple, his first user, creates an account entering the username `Jane Apple` and the password `very secret`. Via an API call from his application to Upvest John is now able to create an account for Jane under his tenancy account with Upvest, by implementing the following call using the API keys object from before:
```python
import json

response = tenancy.register_user('Jane Apple','very secret').raw
recovery_kit = response.json()["recoverykit"]
```
After parsing it to JSON, John can extract the recovery kit with `response["recoverykit"]` and pass it on to Jane

### Wallet Creation
After creating an account Jane wants to create an Ethereum wallet. In order to do that on behalf of Jane, John needs to initialize an OAuth Object with his client credentials and Jane's username and password. After doing so John can easily create a wallet by providing the respective `asset_id` for Ethereum to the `create_wallet()` function. The asset ids can be retrieved via a call to the upvest asset endpoint, using the clientele authentication:
```python
from upvest.tenancy import UpvestClienteleAPI
clientele = UpvestClienteleAPI(CLIENT_ID, CLIENT_SECRET, username, password)

# Listing assets and their ids
asset_id = clientele.list_assets().data[i]["id"]

# Creating a wallet for Jane on Ethereum
ethereum_wallet = clientele.create_wallet(asset_id).data
wallet_address = ethereum_wallet['address']
```
Using the address, Jane is now able to receive funds in her Ethereum wallet on John's platform. Thus, she logs in to her current wallet provider and sends the funds to her newly created wallet.

### Transaction Sending
After a couple of days Jane would like to buy a new roadbike, paying with Ethereum. The address of the seller is: `0x6720d291A72B8673E774A179434C96D21eb85E71` and Jane would like to transfer 1ETH. As quantity is denoted in Wei (Ethereum smallest unit), John will need to implement an automatic transformation of this amount. The transaction can be send via the Upvest API making the following call:
```python
# Retrieving Jane's wallet_id
wallets_of_jane = clientele.list_wallets().data
id_wallet = wallets_of_jane[i]["id"]
recipient = '0x6720d291A72B8673E774A179434C96D21eb85E71'

# Sending the transaction
transaction = clientele.send_transaction('id_wallet', 'asset_id', '1000000000000000000', '4000000000', 'recipient').data
tx_hash = transaction["txhash"]
```

That's it! Jane has successfully sent a transaction and is able to monitor it via [Etherscan](https://etherscan.io).


