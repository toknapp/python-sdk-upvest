import uuid

from . import fresh
from .partials.client_instance import create_tenancy_client
from .partials.static_user import static_user
from .partials.user_creation import create_user

tenancy = create_tenancy_client()


def test_echo():
    """Tests the echo API"""
    tenancy.check_auth()


def test_register_user():
    """Tests an API call to create a user"""
    username = f"upvest_test_{uuid.uuid4()}"
    user = tenancy.users.create(username, fresh.password())
    assert user.username == username
    assert user.recovery_kit is not None


def test_list_user():
    """Tests an API call to get a specific user"""
    user = tenancy.users.get(static_user.username)
    assert user.username == static_user.username


def test_list_users():
    """Tests an API call to get a list of users"""
    users = tenancy.users.list(3)
    assert len(users) == 3
    assert isinstance(users[0].username, str)


def test_change_password():
    """Tests an API call to update a user's password"""
    user, pw = create_user()
    new_pw = fresh.password()
    username = user.username
    user = tenancy.users.get(user.username).update(pw, new_pw)
    user = tenancy.users.get(user.username).update(new_pw, pw)
    assert user.username == username


def test_deregister_user():
    """Tests an API call to deregister a user"""
    user, _ = create_user()
    assert tenancy.users.get(user.username).delete()


def test_list_assets():
    """Tests an API call to deregister a user"""
    assets = tenancy.assets.all()
    assert isinstance(assets, list)
    assert assets[0].id == "51bfa4b5-6499-5fe2-998b-5fb3c9403ac7"
    assert assets[0].name == "Arweave (internal testnet)"
    assert assets[0].symbol == "AR"
    assert assets[0].exponent == 12
    assert assets[0].protocol == "arweave_testnet"
