import uuid

from tests.partials.client_instance import create_tenancy_client

def create_user():
    unique_id = uuid.uuid4()
    username = f'upvest_test{unique_id}'
    password = 'secret'
    tenancy_instance = create_tenancy_client()
    response = tenancy_instance.user.create(username, password)
    return {
        'username': response.data['username'],
        'password': password
    }
