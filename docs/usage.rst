.. _usage:

Usage
===================

This part of the documentation demonstrates how to use Upvest SDK in project.


Tenant creation
---------------

The business "Blockchain4Everyone", founded by `John <https://en.wikipedia.org/wiki/The_man_on_the_Clapham_omnibus>`_, would like to build a platform for Ethereum wallets with easy access and wallet management. Therefore, John visits the `Upvest Signup Page <https://login.upvest.co/sign-up>`_, creates an account, and retrieves his API keys from the account management page. He is now able to create the API Keys Authentication object:

.. code-block:: python

    # API Keys object
    from upvest.tenancy import UpvestTenancyAPI
    tenancy = UpvestTenancyAPI(API_KEY, API_SECRET, API_PASSPHRASE, base_url=BASE_URL)


User creation
-------------

John sets up his platform and soon has the first person signing up for his service. Jane Apple, his first user, creates an account entering the username `Jane Apple` and the password `very secret`. Via an API call from his application's backend to the Upvest API, John creates an account for Jane under his tenancy account with Upvest, by implementing the following call using the API keys object from before:

.. code-block:: python

    user = tenancy.users.create('Jane Apple','very secret')
    recovery_kit = user.recovery_kit


After the request, John can access the recovery kit in the user instance and pass it on to Jane. Recovery kits are encrypted using a public key whose private counterpart is provided to tenants at sign-up on the Upvest Account Management portal, and not stored by Upvest. In case Jane loses her password, John is able to reset her password on her behalf, using her password and his decryption key, after conducting a proper KYC process in order to prevent identity fraud.

Wallet creation
---------------

After creating an account Jane wants to create an Ethereum wallet on John's platform. In order to do that on behalf of Jane, John needs to initialize an OAuth object with his client credentials and Jane's username and password. After doing so, John can easily create a wallet by providing the respective `asset_id` for Ethereum to the `wallets.create()` function. The `asset_id` can be retrieved via a call to the Upvest asset endpoint, using the clientele or tenancy authentication:

.. code-block:: python

    from upvest.clientele import UpvestClienteleAPI
    clientele = UpvestClienteleAPI(CLIENT_ID, CLIENT_SECRET, 'Jane Apple','very secret', base_url=BASE_URL)

.. code-block:: python

    # List assets and their ids
    asset_id = clientele.assets.all()[i].id
    asset_id = tenancy.assets.all()[i].id

    # Create a wallet for Jane on Ethereum with her password and the respective asset_id
    ethereum_wallet = clientele.wallets.create(asset_id, 'very secret')
    wallet_address = ethereum_wallet.address

Using the address, Jane is now able to receive funds in her Ethereum wallet on John's platform. Thus she sends Ethereumfrom her current Ethereum wallet provider and sends the funds to her newly created wallet on John's platform.

Transaction sending
---------------------

After a couple of days, Jane would like to buy a new road bike, paying with Ether. The address of the seller is `0x6720d291A72B8673E774A179434C96D21eb85E71` and Jane needs to transfer 1 ETH. As a quantity it's denoted in `Wei <http://ethdocs.org/en/latest/ether.html#denominations>`_ (Ether's smallest unit), John will need to implement a transformation of this amount. The transaction can be sent via the Upvest API making the following call:

.. code-block:: python

    # Retrieve Jane's wallet_id
    wallets_of_jane = clientele.wallets.all()
    wallet = wallets_of_jane[0]
    recipient = '0x6720d291A72B8673E774A179434C96D21eb85E71'

    # Send the transaction
    transaction = wallet.transactions.create('very secret', 'asset_id', 1000000000000000000, 4000000000, recipient)
    txhash = transaction.txhash

That's it! Jane has successfully sent a transaction and is able to monitor it via `Etherscan <https://etherscan.io>`_.
