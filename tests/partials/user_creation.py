import uuid

from tests.partials.client_instance import create_tenancy_client
from tests import fresh

def create_user():
    username = f'upvest_test{uuid.uuid4()}'
    password = fresh.password()
    tenancy_instance = create_tenancy_client()
    user = tenancy_instance.users.create(username, password)
    return user, password
