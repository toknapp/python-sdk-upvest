import time

from tests.partials.user_creation import create_user
from tests.partials.client_instance import create_oauth_client

def test_create_wallet():
    """Tests an API call to create a wallet"""
    user = create_user()
    clientele = create_oauth_client(user.username,'secret')
    wallet = clientele.wallets.create('deaaa6bf-d944-57fa-8ec4-2dd45d1f5d3f', 'secret')
    assert wallet.protocol == 'ethereum_ropsten'

def test_list_wallet():
    """Tests an API call to list wallets"""
    user = create_user()
    clientele = create_oauth_client(user.username, 'secret')
    clientele.wallets.create('deaaa6bf-d944-57fa-8ec4-2dd45d1f5d3f', 'secret')
    wallets = clientele.wallets.all()
    assert isinstance(wallets, list)
    wallet_id = wallets[0].id
    wallet = clientele.wallets.get(wallet_id)
    assert wallet.protocol == 'ethereum_ropsten'

def test_list_assets():
    """Tests an API call to list assets"""
    user = create_user()
    clientele = create_oauth_client(user.username, 'secret')
    assets = clientele.assets.all() 
    assert isinstance(assets, list)
    assert assets[0].id == '51bfa4b5-6499-5fe2-998b-5fb3c9403ac7'
    assert assets[0].name == 'Arweave (internal testnet)'
    assert assets[0].symbol == 'AR'
    assert assets[0].exponent == 12
    assert assets[0].protocol == 'arweave_testnet'

def test_send_transaction():
    """Tests an API call to send transactions"""
    user = create_user()
    clientele = create_oauth_client(user.username, 'secret')
    wallet = clientele.wallets.create('deaaa6bf-d944-57fa-8ec4-2dd45d1f5d3f','secret')
    transaction =  wallet.transactions.create(
        'secret',
        'deaaa6bf-d944-57fa-8ec4-2dd45d1f5d3f',
        '10000000000000000',
        '41180000000000',
        '0x6720d291a72b8673e774a179434c96d21eb85e71'
    )

    assert transaction.txhash is not None
    assert transaction.sender is not None
    assert transaction.recipient == '0x6720d291a72b8673e774a179434c96d21eb85e71'
    assert transaction.quantity == '10000000000000000'
    assert transaction.fee == '41180000000000'

# def test_list_transaction():
#     """Tests an API call to list a specific transaction"""
#     """Tests an API call to send transactions"""
#     user = create_user()
#     clientele = create_oauth_client(user.username, 'secret')
#     wallet = clientele.wallets.create('deaaa6bf-d944-57fa-8ec4-2dd45d1f5d3f','secret')
#     time.sleep(10)
#     transaction =  wallet.transactions.create(
#         'secret',
#         'deaaa6bf-d944-57fa-8ec4-2dd45d1f5d3f',
#         '10000000000000000',
#         '41180000000000',
#         '0x6720d291a72b8673e774a179434c96d21eb85e71'
#     )
#     transaction_txhash = transaction.txhash

#     transaction_retrieved = wallet.transactions.get(transaction_txhash)
#     time.sleep(20)
#     assert transaction_retrieved.txhash is not None
#     assert transaction_retrieved.sender is not None
#     assert transaction_retrieved.recipient == '0x6720d291a72b8673e774a179434c96d21eb85e71'
#     assert transaction_retrieved.quantity == '10000000000000000'
#     assert transaction_retrieved.fee == '41180000000000'
