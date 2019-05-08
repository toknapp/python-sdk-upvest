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
Create an API key pair within the dashboard.

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
All tenancy related operations must be using the API Keys authentication, whereas all actions on a user's behalf need to be authenticated via OAuth. The API calls are built along with those two authentication objects.

The methods allow for passing parameters if needed. If the required arguments are not provided, the respective error will be raised.

### Response Objects
The response objects across all endpoints ("users", "wallets", "assets", "transactions") follow the same structure. If you retrieve more than one object (for example: `tenancy.users.all()`, a list of objects will be returned.

#### User Object
The user response object has the following attributes:
```python
UserObject.username
UserObject.recoverykit #only if just created
```

#### Wallet Object
The wallet response object has the following attributes:
```python
WalletObject.transactions
WalletObject.id
WalletObject.balances
WalletObject.protocol
WalletObject.address
WalletObject.status
```

#### Asset Object
The transaction response object has the following attributes:
```python
AssetObject.id
AssetObject.name
AssetObject.symbol
AssetObject.exponent
AssetObject.protocol
AssetObject.metadata
```

#### Transaction Object
The transaction response object has the following attributes:
```python
TransactionObject.path
TransactionObject.txhash
TransactionObject.sender
TransactionObject.recipient
TransactionObject.quantity
TransactionObject.fee
```

Usage
------
### Tenancy
#### User Endpoint
##### Create a user
```python
tenancy.users.create('username','password')
```
##### List a user
```python
tenancy.users.get('username')
```
##### List all users under tenancy
```python
tenancy.users.all()
```
##### List a specific number of users under tenancy
```python
tenancy.users.list(40)
```
##### Change password of a user
```python
tenancy.users.get('username').update('current_password', 'new_password')
```
##### Deregister a user
```python
tenancy.user.get('username').delete('username')
```

### Clientele
#### Assets
##### List available assets
```python
clientele.assets.all()
```

#### Wallets
##### Create a wallet for a user
```python
clientele.wallets.create('asset_id')
```
##### List all wallets for a user
```python
clientele.wallets.all()
```
##### List a specific number of assets
```python
clientele.assets.list(40)
```
##### List specific wallet for a user
```python
clientele.wallet.get('wallet_id')
```

#### Transactions
##### Send transaction
```python
wallet = clientele.wallets.create('asset_id','secret')
wallet.transactions.create('secret', 'asset_id', 'quantity', 'fee', 'recipient')
```

Usage
------
## Tutorial
### Tenant Creation
The business "Successful blockchain project", founded by John Doe, would like to build a platform for Ethereum wallets with easy access and wallet management. Therefore, John visits the [Upvest Signup Page](https://login.upvest.co/sign-up), creates an account, and retrieves his API keys from the account management page. He is now able to create the API keys Authentication Object:
```python
# API Keys Object
from upvest.tenancy import UpvestTenancyAPI
tenancy = UpvestTenancyAPI(API_KEY, API_SECRET, API_PASSPHRASE)
```

### User Creation
John sets up his platform and soon has the first person signing up for his service. Jane Apple, his first user, creates an account entering the username `Jane Apple` and the password `very secret`. Via an API call from his application to Upvest John is now able to create an account for Jane under his tenancy account with Upvest, by implementing the following call using the API keys object from before:
```python
import json

user = tenancy.users.create('Jane Apple','very secret').raw
recovery_kit = user.recovery_kit
```
After the request, John can access the recovery kit in the user instance and pass it on to Jane.

### Wallet Creation
After creating an account Jane wants to create an Ethereum wallet. In order to do that on behalf of Jane, John needs to initialize an OAuth Object with his client credentials and Jane's username and password. After doing so John can easily create a wallet by providing the respective `asset_id` for Ethereum to the `create()` function. The asset ids can be retrieved via a call to the Upvest asset endpoint, using the clientele authentication:
```python
from upvest.tenancy import UpvestClienteleAPI
clientele = UpvestClienteleAPI(CLIENT_ID, CLIENT_SECRET, username, password)

# Listing assets and their ids
asset_id = clientele.assets.all()[i].id

# Creating a wallet for Jane on Ethereum
ethereum_wallet = clientele.wallets.create(asset_id)
wallet_address = ethereum_wallet.address
```
Using the address, Jane is now able to receive funds in her Ethereum wallet on John's platform. Thus, she logs in to her current wallet provider and sends the funds to her newly created wallet.

### Transaction Sending
After a couple of days, Jane would like to buy a new road bike, paying with Ethereum. The address of the seller is: `0x6720d291A72B8673E774A179434C96D21eb85E71` and Jane would like to transfer 1ETH. As quantity is denoted in Wei (Ethereum smallest unit), John will need to implement an automatic transformation of this amount. The transaction can be sent via the Upvest API making the following call:
```python
# Retrieving Jane's wallet_id
wallets_of_jane = clientele.wallets.all()
wallet = wallets_of_jane[i]
recipient = '0x6720d291A72B8673E774A179434C96D21eb85E71'

# Sending the transaction
transaction = clientele.wallet.transactions.create('secret', 'asset_id', '1000000000000000000', '4000000000', 'recipient')
tx_hash = transaction.txhash
```

That's it! Jane has successfully sent a transaction and is able to monitor it via [Etherscan](https://etherscan.io).


