import uuid

from tests.partials.client_instance import create_tenancy_client
from tests.partials.user_creation import create_user

tenancy_instance = create_tenancy_client()

def test_register_user():
    """Tests an API call to create a user"""
    unique_id = uuid.uuid4()
    response = tenancy_instance.users.create(f'upvest_test_{unique_id}','secret')
    assert response.status_code == 201
    assert response.data['username'] == f'upvest_test_{unique_id}'

def test_list_user():
    """Tests an API call to get a specific user"""
    user = create_user()
    user_instance = tenancy_instance.users.get(user['username'])
    assert user_instance.username == user['username']

def test_list_users():
    """Tests an API call to get a list of usersr"""
    response = tenancy_instance.users.all()
    assert response.status_code == 200

def test_change_password():
    """Tests an API call to update a user's password"""
    user = create_user()
    response = tenancy_instance.users.get(user['username']).update('secret','new_secret')
    assert response.status_code == 200
    response = tenancy_instance.users.get(user['username']).update('new_secret', 'secret')
    assert response.status_code == 200

def test_deregister_user():
    """Tests an API call to deregister a user"""
    user = create_user()
    response = tenancy_instance.users.get(user['username']).delete()
    assert response.status_code == 204
