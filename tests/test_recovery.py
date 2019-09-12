import time
import uuid

from upvest.config import PRIVATE_KEY_BASE64

from . import fresh
from .partials.client_instance import create_tenancy_client, create_oauth_client
from .partials.user_creation import create_user
from .test_clientele_api import ETHEREUM_ROPSTEN_ASSET_ID

tenancy = create_tenancy_client()


def test_recovery():
    """Tests user password recovery flow"""
    username = f"upvest_test_{uuid.uuid4()}"

    old_password, new_password = [fresh.password() for _ in range(2)]
    user = tenancy.users.create(username, old_password, raw_recovery_kit=True, asset_ids=[ETHEREUM_ROPSTEN_ASSET_ID])

    clientele = create_oauth_client(username, old_password)
    clientele.check_auth()

    tenancy.recover(
        recovery_kit_base64=user.recovery_kit, private_key_base64=PRIVATE_KEY_BASE64, new_password=new_password
    )

    for i in range(60):
        time.sleep(2)
        wallet = clientele.wallets.all()[0]
        if wallet.status == "ACTIVE":
            break
    else:
        assert False, "wallet did not become active in time"

    create_oauth_client(username, new_password).check_auth()
