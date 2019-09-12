import base64

from google.protobuf.json_format import MessageToDict
from nacl.public import PrivateKey, SealedBox

from upvest.authentication import KeyAuth
from upvest.config import UPVEST_API_TARGET
from upvest.exceptions import RecoveryFailedError
from upvest.model import Assets, Users
from upvest.proto import RecoveryKit
from upvest.utils import Request, Response, verify_echo


class UpvestTenancyAPI:
    def __init__(self, api_key, api_secret, api_passphrase, base_url=None, user_agent=None):
        base_url = base_url or UPVEST_API_TARGET
        self.auth_instance = KeyAuth(
            api_key=api_key,
            api_secret=api_secret,
            api_passphrase=api_passphrase,
            base_url=base_url,
            user_agent=user_agent,
        )
        self.users = Users(self.auth_instance)
        self.assets = Assets(self.auth_instance)

    def check_auth(self):
        verify_echo(self.auth_instance, "/tenancy/echo-signed")

    def recover_with_seed(self, seed, seedhash, user_id, password):
        path = "/tenancy/recover/"

        # Set username and password for the user
        body = {"seed": seed, "seedhash": seedhash, "user_id": user_id, "password": password}
        response = Response(Request().post(auth_instance=self.auth_instance, path=path, body=body))
        if not response.data["success"]:
            raise RecoveryFailedError("Recovery unsuccessful")

    def recover(self, recovery_kit_base64, private_key_base64, new_password):
        cipher = base64.b64decode(recovery_kit_base64)

        pk = PrivateKey(base64.b64decode(private_key_base64))
        proto = SealedBox(pk).decrypt(cipher)

        kit = RecoveryKit()
        kit.ParseFromString(proto)

        seed = MessageToDict(kit.seed, including_default_value_fields=True)

        self.recover_with_seed(seed=seed, seedhash=kit.seedhash, user_id=kit.user_id, password=new_password)
