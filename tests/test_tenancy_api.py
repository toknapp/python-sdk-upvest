import uuid
import pytest

from tests.partials.client_instance import create_tenancy_client
from tests.partials.user_creation import create_user

tenancy = create_tenancy_client()

def test_register_user():
    """Tests an API call to create a user"""
    unique_id = uuid.uuid4()
    user = tenancy.users.create(f'upvest_test_{unique_id}','secret')
    assert user.username == f'upvest_test_{unique_id}'
    assert user.recovery_kit is not None

def test_list_user():
    """Tests an API call to get a specific user"""
    user = tenancy.users.get('alex_test')
    assert user.username == 'alex_test'

def test_list_155_users():
    """Tests an API call to get a list of usersr"""
    users = tenancy.users.list(155)
    assert len(users) == 155
    assert isinstance(users[0].username, str)

def test_change_password():
    """Tests an API call to update a user's password"""
    user = create_user()
    username = user.username
    user = tenancy.users.get(user.username).update('secret','new_secret')
    user = tenancy.users.get(user.username).update('new_secret', 'secret')
    assert user.username == username

def test_deregister_user():
    """Tests an API call to deregister a user"""
    user = create_user()
    assert tenancy.users.get(user.username).delete() is None

def test_list_assets():
    """Tests an API call to deregister a user"""
    assets = tenancy.assets.all()
    assert isinstance(assets, list)
    assert assets[0].id == '51bfa4b5-6499-5fe2-998b-5fb3c9403ac7'
    assert assets[0].name == 'Arweave (internal testnet)'
    assert assets[0].symbol == 'AR'
    assert assets[0].exponent == 12
    assert assets[0].protocol == 'arweave_testnet'
