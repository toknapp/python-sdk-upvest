import time

from tests.partials.user_creation import create_user
from tests.partials.client_instance import create_oauth_client

def test_create_wallet():
    """Tests an API call to create a wallet"""
    user = create_user()
    oauth_instance = create_oauth_client(user['username'],user['password'])
    response = oauth_instance.wallets.create('deaaa6bf-d944-57fa-8ec4-2dd45d1f5d3f')
    assert response.status_code == 201

def test_list_wallets():
    """Tests an API call to list wallets"""
    user = create_user()
    oauth_instance = create_oauth_client(user['username'], user['password'])
    oauth_instance.wallets.create('deaaa6bf-d944-57fa-8ec4-2dd45d1f5d3f')
    response = oauth_instance.wallets.all()
    assert response.status_code == 200

    id = response.data[0]['id']
    response = oauth_instance.wallets.get(id)
    assert response.status_code == 200


def test_list_assets():
    """Tests an API call to list assets"""
    user = create_user()
    oauth_instance = create_oauth_client(user['username'], user['password'])
    response = oauth_instance.assets.all() 
    assert response.status_code == 200


def test_send_transaction():
    """Tests an API call to send transactions"""
    user = create_user()
    oauth_instance = create_oauth_client(user['username'], user['password'])
    wallet_id = oauth_instance.wallets.create('deaaa6bf-d944-57fa-8ec4-2dd45d1f5d3f').data['id']
    response = oauth_instance.transactions.send(
        wallet_id, 
        'deaaa6bf-d944-57fa-8ec4-2dd45d1f5d3f', 
        '10000000000000000', 
        '41180000000000', 
        '0x6720d291a72b8673e774a179434c96d21eb85e71'
    )
    assert response.status_code == 201
    assert response.data['txhash'] is not None


# def test_list_transaction():
#     """Tests an API call to list a specific transaction"""
#     username = f'upvest_test_{rand_int}'
#     create_user(tenancy_instance, username, 'secret')
#     oauth_instance = create_oauth_client(username, 'secret')
#     wallet_creation_response = oauth_instance.create_wallet('deaaa6bf-d944-57fa-8ec4-2dd45d1f5d3f')
#     wallet_id = wallet_creation_response.json()['id']
#     response = oauth_instance.send_transaction(wallet_id, 'deaaa6bf-d944-57fa-8ec4-2dd45d1f5d3f', '1000000000000000', '41180000000000', '0x6720d291a72b8673e774a179434c96d21eb85e71')
#     tx_hash = response.json()['txhash']
#     response = oauth_instance.list_transaction(tx_hash)
#     assert response.status_code == 200
