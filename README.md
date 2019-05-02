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
For more information on the OAuth concept, please refer to our [documentation](https://doc.upvest.co/docs/oauth2-authentication)
Retrieve your client credentials from the dashboard.

Next, create an UpvestClienteleAPI object in order to authenticate your API calls on behalf of a user:
```python
from upvest.clientele import UpvestClienteleAPI
clientele = UpvestClienteleAPI(CLIENT_ID, CLIENT_SECRET, username, password)
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
#### Change password of a user
```python
tenancy.deregister_user('username')
```

### Clientele
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