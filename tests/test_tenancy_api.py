import uuid
import pytest

from tests.partials.client_instance import create_tenancy_client
from tests.partials.user_creation import create_user

tenancy_instance = create_tenancy_client()

def test_register_user():
    """Tests an API call to create a user"""
    unique_id = uuid.uuid4()
    user = tenancy_instance.users.create(f'upvest_test_{unique_id}','secret')
    assert user.username == f'upvest_test_{unique_id}'
    assert user.recovery_kit is not None

def test_list_user():
    """Tests an API call to get a specific user"""
    test_user = create_user()
    user = tenancy_instance.users.get(test_user.username)
    assert user.username == test_user.username

# def test_list_users():
#     """Tests an API call to get a list of usersr"""
#     users = tenancy_instance.users.all()
#     assert len(users) == 2000

def test_change_password():
    """Tests an API call to update a user's password"""
    user = create_user()
    username = user.username
    user = tenancy_instance.users.get(user.username).update('secret','new_secret')
    user = tenancy_instance.users.get(user.username).update('new_secret', 'secret')
    assert user.username == username


def test_deregister_user():
    """Tests an API call to deregister a user"""
    user = create_user()
    assert tenancy_instance.users.get(user.username).delete() is None

# def test_access_non_existing_previous_page():
#     """Tests whether exception is thrown if there is no previous page in results"""
#     with pytest.raises(Exception) as e:
#         tenancy_instance.users.all().previous()
#     assert str(e.value) == 'There is no previous page'

# def test_next_iterator():
#     """Tests whether next iterator works"""
#     results = tenancy_instance.users.all().next().data
#     assert len(results) == 10
