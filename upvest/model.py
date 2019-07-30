import hashlib
from base64 import b64encode
from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit

from upvest.config import API_VERSION
from upvest.utils import Request, Response


# Endpoint related objects
class UserInstance:
    def __init__(self, auth_instance, username, recovery_kit=None):
        self.path = "/tenancy/users/"
        self.auth_instance = auth_instance
        self.username = username
        self.recovery_kit = recovery_kit

    def update(self, password, new_password):
        # Provide current and new password
        body = {"old_password": password, "new_password": new_password}
        response = Response(
            Request().patch(auth_instance=self.auth_instance, path=self.path + self.username, body=body)
        )
        username = response.data["username"]
        return UserInstance(response, username)

    def delete(self):
        response = Response(
            Request().delete(auth_instance=self.auth_instance, path=self.path + self.username, body=None)
        )
        return response.status_code == 204

    def __eq__(self, other):
        return self.username == other.username


class Users:
    def __init__(self, auth_instance):
        self.path = "/tenancy/users/"
        self.auth_instance = auth_instance

    def create(self, username, password):
        # Set username and password for the user
        body = {"username": username, "password": password}
        response = Response(Request().post(auth_instance=self.auth_instance, path=self.path, body=body))
        username = response.data["username"]
        recovery_kit = response.data["recoverykit"]
        return UserInstance(self.auth_instance, username, recovery_kit)

    def get(self, username):
        response = Response(Request().get(auth_instance=self.auth_instance, path=self.path + username))
        username = response.data["username"]
        return UserInstance(self.auth_instance, username)

    def list(self, count):
        # Retrieve subset of users
        MAX_PAGE_SIZE = 100
        array_of_users = []
        path = f"/tenancy/users/?page_size={MAX_PAGE_SIZE}"
        listed_count = 0

        while listed_count < count:
            response = Response(Request().get(auth_instance=self.auth_instance, path=path))
            for user in response.data:
                username = user["username"]
                array_of_users.append(UserInstance(self.auth_instance, username))
                listed_count += 1
                if listed_count >= count:
                    break
            if response.raw.json()["next"]:
                page_size = min(MAX_PAGE_SIZE, count - listed_count)
                path = response.raw.json()["next"].split(API_VERSION)[-1]
                path_parts = list(urlsplit(path))
                query = parse_qs(path_parts[3])
                query["page_size"] = [page_size]
                path_parts[3] = urlencode(query, doseq=True)
                path = urlunsplit(path_parts)
            else:
                break
        return array_of_users

    def all(self):
        MAX_PAGE_SIZE = 100
        array_of_users = []
        path = "/tenancy/users/?{MAX_PAGE_SIZE}"

        while True:
            response = Response(Request().get(auth_instance=self.auth_instance, path=path))
            for user in response.data:
                username = user["username"]
                array_of_users.append(UserInstance(self.auth_instance, username))
            if response.raw.json()["next"]:
                path = response.raw.json()["next"].split(API_VERSION)[-1]
                path_parts = list(urlsplit(path))
                query = parse_qs(path_parts[3])
                query["page_size"] = [MAX_PAGE_SIZE]
                path_parts[3] = urlencode(query, doseq=True)
                path = urlunsplit(path_parts)
            else:
                break
        return array_of_users


class AssetInstance:
    def __init__(self, **asset_attr):
        self.id = asset_attr["id"]
        self.name = asset_attr["name"]
        self.symbol = asset_attr["symbol"]
        self.exponent = asset_attr["exponent"]
        self.protocol = asset_attr["protocol"]
        self.metadata = asset_attr["metadata"]


class Assets:
    def __init__(self, auth_instance):
        self.path = "/assets/"
        self.auth_instance = auth_instance

    def all(self):
        MAX_PAGE_SIZE = 100
        array_of_assets = []
        path = "/assets/?{MAX_PAGE_SIZE}"

        while True:
            response = Response(Request().get(auth_instance=self.auth_instance, path=path))
            for asset in response.data:
                array_of_assets.append(AssetInstance(**asset))
            if response.raw.json()["next"]:
                path = response.raw.json()["next"].split(API_VERSION)[-1]
                path_parts = list(urlsplit(path))
                query = parse_qs(path_parts[3])
                query["page_size"] = [MAX_PAGE_SIZE]
                path_parts[3] = urlencode(query, doseq=True)
                path = urlunsplit(path_parts)
            else:
                break
        return array_of_assets


class ECDSASignature:
    def __init__(self, signed_hash, j):
        self.algorithm = j["algorithm"]
        if self.algorithm != "ECDSA":
            raise ValueError(f"unsupported algorithm: {self.algorithm}")

        self.curve = j["curve"]
        self.x = j["public_key"]["x"]
        self.y = j["public_key"]["y"]
        self.r = j["r"]
        self.s = j["s"]
        self.signed_hash = signed_hash

        if self.curve == "secp256k1":
            self.recover = j["recover"]
        else:
            # TODO: is pubkey recovery possible for other curves?
            pass


class WalletInstance:
    def __init__(self, auth_instance, **wallet_attr):
        self.auth_instance = auth_instance
        self.transactions = Transactions(auth_instance, wallet_attr["id"])
        self.id = wallet_attr["id"]
        self.path = f"/kms/wallets/{self.id}"
        self.balances = wallet_attr["balances"]
        self.protocol = wallet_attr["protocol"]
        self.address = wallet_attr["address"]
        self.status = wallet_attr["status"]

    def sign(self, password, message=None, to_sign_hash=None, hash_algorithm="SHA256"):
        if to_sign_hash is None and message is not None:
            if not isinstance(message, (bytes, bytearray)):
                raise TypeError("message argument is not a bytes-like object")

            if hash_algorithm == "SHA256":
                to_sign_hash = hashlib.sha256(message).digest()
            else:
                raise ValueError(f"unsupported hash_algorithm: {hash_algorithm}")

        if to_sign_hash is None:
            raise ValueError(f"neither message nor to_sign_hash were provided")

        body = {"password": password, "to_sign": str(b64encode(to_sign_hash), "UTF-8"), "output_format": "int"}
        rsp = Response(Request().post(auth_instance=self.auth_instance, path=f"{self.path}/sign", body=body))
        return ECDSASignature(signed_hash=to_sign_hash, j=rsp.data)


class Wallets:
    def __init__(self, auth_instance):
        self.path = "/kms/wallets/"
        self.auth_instance = auth_instance

    def create(self, asset_id, password):
        # Get desired asset id from assets list
        # Provide password and asset_id for wallet creation
        body = {"password": password, "asset_id": asset_id}
        response = Response(Request().post(auth_instance=self.auth_instance, path=self.path, body=body))
        return WalletInstance(self.auth_instance, **response.data)

    def get(self, wallet_id):
        # Retrieve specific wallet for a user
        response = Response(Request().get(auth_instance=self.auth_instance, path=self.path + wallet_id))
        return WalletInstance(self.auth_instance, **response.data)

    def list(self, count):
        # Retrieve subset of wallets
        MAX_PAGE_SIZE = 100
        array_of_wallets = []
        path = f"/kms/wallets/?page_size={MAX_PAGE_SIZE}"
        listed_count = 0

        while listed_count < count:
            response = Response(Request().get(auth_instance=self.auth_instance, path=path))
            for wallet in response.data:
                array_of_wallets.append(WalletInstance(self.auth_instance, **wallet))
                listed_count += 1
                if listed_count >= count:
                    break
            if response.raw.json()["next"]:
                page_size = min(MAX_PAGE_SIZE, count - listed_count)
                path = response.raw.json()["next"].split(API_VERSION)[-1]
                path_parts = list(urlsplit(path))
                query = parse_qs(path_parts[3])
                query["page_size"] = [page_size]
                path_parts[3] = urlencode(query, doseq=True)
                path = urlunsplit(path_parts)
            else:
                break
        return array_of_wallets

    def all(self):
        # Retrieve subset of wallets
        MAX_PAGE_SIZE = 100
        array_of_wallets = []
        path = f"/kms/wallets/?page_size={MAX_PAGE_SIZE}"

        while True:
            response = Response(Request().get(auth_instance=self.auth_instance, path=path))
            for wallet in response.data:
                array_of_wallets.append(WalletInstance(self.auth_instance, **wallet))
            if response.raw.json()["next"]:
                path = response.raw.json()["next"].split(API_VERSION)[-1]
                path_parts = list(urlsplit(path))
                query = parse_qs(path_parts[3])
                query["page_size"] = [MAX_PAGE_SIZE]
                path_parts[3] = urlencode(query, doseq=True)
                path = urlunsplit(path_parts)
            else:
                break
        return array_of_wallets


class TransactionInstance:
    def __init__(self, **transaction_attr):
        self.path = "/kms/wallets/"
        self.id = transaction_attr["id"]
        self.txhash = transaction_attr["txhash"]
        self.sender = transaction_attr["sender"]
        self.recipient = transaction_attr["recipient"]
        self.asset_id = transaction_attr["asset_id"]
        self.quantity = int(transaction_attr["quantity"])
        self.fee = int(transaction_attr["fee"])
        self.status = transaction_attr["status"]


class Transactions:
    def __init__(self, auth_instance, wallet_id):
        self.path = "/kms/wallets/"
        self.auth_instance = auth_instance
        self.wallet_id = wallet_id

    def create(self, password, asset_id, quantity, fee, recipient):
        # Provide password and asset_id for wallet creation
        body = {
            "password": password,
            "asset_id": asset_id,
            "quantity": str(quantity),
            "fee": str(fee),
            "recipient": recipient,
        }
        response = Response(
            Request().post(
                auth_instance=self.auth_instance, path=f"{self.path}{self.wallet_id}/transactions/", body=body
            )
        )
        return TransactionInstance(**response.data)

    def get(self, transaction_id):
        # Define tx endpoint
        response = Response(
            Request().get(
                auth_instance=self.auth_instance, path=f"{self.path}{self.wallet_id}/transactions/{transaction_id}"
            )
        )
        return TransactionInstance(**response.data)

    def list(self, count):
        # Retrieve subset of wallets
        MAX_PAGE_SIZE = 100
        array_of_transactions = []
        path = f"{self.path}{self.wallet_id}/transactions/?page_size={MAX_PAGE_SIZE}"
        listed_count = 0

        while listed_count < count:
            response = Response(Request().get(auth_instance=self.auth_instance, path=path))
            for transaction in response.data:
                array_of_transactions.append(TransactionInstance(**transaction))
                listed_count += 1
                if listed_count >= count:
                    break
            if response.raw.json()["next"]:
                page_size = min(MAX_PAGE_SIZE, count - listed_count)
                path = response.raw.json()["next"].split(API_VERSION)[-1]
                path_parts = list(urlsplit(path))
                query = parse_qs(path_parts[3])
                query["page_size"] = [page_size]
                path_parts[3] = urlencode(query, doseq=True)
                path = urlunsplit(path_parts)
            else:
                break
        return array_of_transactions

    def all(self):
        MAX_PAGE_SIZE = 100
        array_of_transactions = []
        path = f"{self.path}{self.wallet_id}/transactions/?page_size={MAX_PAGE_SIZE}"

        while True:
            response = Response(Request().get(auth_instance=self.auth_instance, path=path))
            for transaction in response.data:
                array_of_transactions.append(TransactionInstance(**transaction))
            if response.raw.json()["next"]:
                path = response.raw.json()["next"].split(API_VERSION)[-1]
                path_parts = list(urlsplit(path))
                query = parse_qs(path_parts[3])
                query["page_size"] = [MAX_PAGE_SIZE]
                path_parts[3] = urlencode(query, doseq=True)
                path = urlunsplit(path_parts)
            else:
                break
        return array_of_transactions
