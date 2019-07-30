import pytest

from tests.partials.client_instance import create_tenancy_client

tenancy_instance = create_tenancy_client()


def test_user_creation_with_non_ascii():
    """Tests an API call to create a user with non-ASCII characters"""
    with pytest.raises(Exception) as e:
        tenancy_instance.users.create("©", "©")
    assert str(e.value) == "Forbidden characters present, please remove"
