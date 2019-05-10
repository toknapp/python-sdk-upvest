Upvest Python SDK
=================

Installation
------
The Upvest SDK is available on [PYPI](https://pypi.org). Install with pip:
```python
pip install upvest
```

Documentation
------
In order to retrieve your API credentials for using this Python client, you'll need to [sign up with Upvest](https://login.upvest.co/sign-up).

### API Keys Authentication
Upvest defines the notion of ‘tenants’, which represent customers that build their platform upon the Upvest API. The end-users of the tenant (i.e. your customers), are referred to as ‘clients’. A tenant is able to manage their users directly (CRUD operations for the user instance) and is also able to initiate actions on the user's behalf (create wallets, send transactions).

The authentication via API keys and secret allows you to perform all tenant related operations.
Please create an API key pair within the [Upvest account management](https://login.upvest.co/).

The default `BASE_URL` for both authentication objects is 'https://api.playground.upvest.co', but feel free to adjust it, once you retrieve your live keys.
Next, create an `UpvestTenancyAPI` object in order to authenticate your API calls:
```python
from upvest.tenancy import UpvestTenancyAPI
tenancy = UpvestTenancyAPI(API_KEY, API_SECRET, API_PASSPHRASE, base_url=BASE_URL) # or base_url=None to use the playground environment (default)
```

### OAuth Authentication
The authentication via OAuth allows you to perform operations on behalf of your user.
For more information on the OAuth concept, please refer to our [documentation](https://doc.upvest.co/docs/oauth2-authentication).
Again, please retrieve your client credentials from the [Upvest account management](https://login.upvest.co/).

Next, create an `UpvestClienteleAPI` object with these credentials and your user authentication data in order to authenticate your API calls on behalf of a user:
```python
from upvest.clientele import UpvestClienteleAPI
clientele = UpvestClienteleAPI(CLIENT_ID, CLIENT_SECRET, username, password, base_url=BASE_URL) # or base_url=None to use the playground environment (default)
```

### API Calls
All tenancy related operations must be authenticated using the API Keys Authentication, whereas all actions on a user's behalf need to be authenticated via OAuth. The API calls are built along with those two authentication objects.

The methods allow for passing parameters if needed. If the required arguments are not provided, a respective error will be raised.

### Response objects
The response objects are designed around users, wallets, transactions and assets. If you retrieve more than one object (for example: `tenancy.users.all()`) a list of those objects will be returned.

#### User object
The user response object has the following properties:
```python
user = tenancy.users.get('mr-foo')
user.username
user.recoverykit # is None if not just created
```

#### Wallet object
The wallet response object has the following properties:
```python
wallet = clientele.wallets.get('wallet_id')
wallet.transactions
wallet.id
wallet.balances
wallet.protocol
wallet.address
wallet.status
```

#### Asset object
The transaction response object has the following properties:
```python
asset, *rest = clientele.assets.all()
asset.id
asset.name
asset.symbol
asset.exponent
asset.protocol
asset.metadata
```

#### Transaction object
The transaction response object has the following properties:
```python
transaction = wallet.transactions.get('transaction_id')
transaction.id
transaction.path
transaction.hash
transaction.sender
transaction.recipient
transaction.quantity
transaction.fee
```

Usage
------
### Tenancy
#### User management
##### Create a user
```python
user = tenancy.users.create('username','password')
```
##### Retrieve a user
```python
user = tenancy.users.get('username')
```
##### List all users under tenancy
```python
users = tenancy.users.all()
```
##### List a specific number of users under tenancy
```python
users = tenancy.users.list(10)
```
##### Change password of a user
```python
user = tenancy.users.get('username').update(password='current_password', new_password='new_password')
```
##### Delete a user
```python
tenancy.user.get('username').delete()
```

### Clientele
#### Assets
##### List available assets
```python
assets = clientele.assets.all()
```
Note that it's also possible to retrieve the same list from `tenancy.assets.all()`.

#### Wallets
##### Create a wallet for a user
```python
wallet = clientele.wallets.create('asset_id', 'password')
```
##### Retrieve specific wallet for a user
```python
wallet = clientele.wallet.get('wallet_id')
```
##### List all wallets for a user
```python
wallets = clientele.wallets.all()
```
##### List a specific number of wallets
```python
wallets = clientele.wallets.list(40)
```

#### Transactions
##### Create transaction
```python
wallet = clientele.wallets.create('asset_id','secret')
transaction = wallet.transactions.create('secret', 'asset_id', 'quantity', 'fee', 'recipient')
```
#### Retrieve specific transaction
```python
wallet = clientele.wallets.create('asset_id','secret')
id = wallet.transactions.all()[i].id
transaction = wallet.transactions.get(id)
```
##### List all transactions of a wallet for a user
```python
wallet = clientele.wallets.create('asset_id','secret')
transactions = wallet.transactions.all()
```
##### List a specific number of transactions of a wallet for a user
```python
wallet = clientele.wallets.create('asset_id','secret')
transactions = wallet.transactions.list(8)
```

Usage
------

### Tenant creation
The business "Blockchain4Everyone", founded by [John](https://en.wikipedia.org/wiki/The_man_on_the_Clapham_omnibus), would like to build a platform for Ethereum wallets with easy access and wallet management. Therefore, John visits the [Upvest Signup Page](https://login.upvest.co/sign-up), creates an account, and retrieves his API keys from the account management page. He is now able to create the API Keys Authentication object:
```python
# API Keys object
from upvest.tenancy import UpvestTenancyAPI
tenancy = UpvestTenancyAPI(API_KEY, API_SECRET, API_PASSPHRASE)
```

### User creation
John sets up his platform and soon has the first person signing up for his service. Jane Apple, his first user, creates an account entering the username `Jane Apple` and the password `very secret`. Via an API call from his application's backend to the Upvest API, John creates an account for Jane under his tenancy account with Upvest, by implementing the following call using the API keys object from before:
```python
user = tenancy.users.create('Jane Apple','very secret')
recovery_kit = user.recovery_kit
```
After the request, John can access the recovery kit in the user instance and pass it on to Jane. Recovery kits are encrypted using a public key whose private counterpart is provided to tenants at sign-up on the Upvest Account Management portal, and not stored by Upvest. In case Jane loses her password, John is able to reset her password on her behalf, using her password and his decryption key, after conducting a proper KYC process in order to prevent identity fraud.

### Wallet creation
After creating an account Jane wants to create an Ethereum wallet on John's platform. In order to do that on behalf of Jane, John needs to initialize an OAuth object with his client credentials and Jane's username and password. After doing so, John can easily create a wallet by providing the respective `asset_id` for Ethereum to the `wallets.create()` function. The `asset_id` can be retrieved via a call to the Upvest asset endpoint, using the clientele or tenancy authentication:
```python
from upvest.tenancy import UpvestClienteleAPI
clientele = UpvestClienteleAPI(CLIENT_ID, CLIENT_SECRET, username, password)

# List assets and their ids
asset_id = clientele.assets.all()[i].id
asset_id = tenancy.assets.all()[i].id

# Create a wallet for Jane on Ethereum with her password and the respective asset_id
ethereum_wallet = clientele.wallets.create(asset_id, 'very_secret')
wallet_address = ethereum_wallet.address
```
Using the address, Jane is now able to receive funds in her Ethereum wallet on John's platform. Thus she sends Ethereumfrom her current Ethereum wallet provider and sends the funds to her newly created wallet on John's platform.

### Transaction sending
After a couple of days, Jane would like to buy a new road bike, paying with Ether. The address of the seller is `0x6720d291A72B8673E774A179434C96D21eb85E71` and Jane needs to transfer 1 ETH. As a quantity it's denoted in [Wei](http://ethdocs.org/en/latest/ether.html#denominations) (Ether's smallest unit), John will need to implement a transformation of this amount. The transaction can be sent via the Upvest API making the following call:
```python
# Retrieve Jane's wallet_id
wallets_of_jane = clientele.wallets.all()
wallet = wallets_of_jane[i]
recipient = '0x6720d291A72B8673E774A179434C96D21eb85E71'

# Send the transaction
transaction = wallet.transactions.create('secret', 'asset_id', 1000000000000000000, 4000000000, 'recipient')
txhash = transaction.txhash
```

That's it! Jane has successfully sent a transaction and is able to monitor it via [Etherscan](https://etherscan.io).
