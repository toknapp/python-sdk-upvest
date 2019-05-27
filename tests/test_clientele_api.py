from .partials.user_creation import create_user
from .partials.client_instance import create_oauth_client
from . import fresh

from py_ecc.secp256k1 import ecdsa_raw_recover
from binascii import hexlify
import hashlib, sha3, bitcoin

ETHEREUM_ROPSTEN_ASSET_ID = 'deaaa6bf-d944-57fa-8ec4-2dd45d1f5d3f'
BITCOIN_TESTNET_ASSET_ID = 'a3c18f74-935e-5d75-bd3c-ce0fb5464414'

def test_create_wallet():
    """Tests an API call to create a wallet"""
    user, pw = create_user()
    clientele = create_oauth_client(user.username, pw)
    wallet = clientele.wallets.create(ETHEREUM_ROPSTEN_ASSET_ID, pw)
    assert wallet.protocol == 'ethereum_ropsten'

def test_list_wallet():
    """Tests an API call to list wallets"""
    user, pw = create_user()
    clientele = create_oauth_client(user.username, pw)
    clientele.wallets.create(ETHEREUM_ROPSTEN_ASSET_ID, pw)
    wallets = clientele.wallets.all()
    assert isinstance(wallets, list)
    wallet_id = wallets[0].id
    wallet = clientele.wallets.get(wallet_id)
    assert wallet.protocol == 'ethereum_ropsten'

def test_list_wallets():
    """Tests an API call to list wallets"""
    clientele = create_oauth_client('alex_test', 'secret')
    wallets = clientele.wallets.list(2)
    assert len(wallets) == 2

def test_all_wallets():
    """Tests an API call to list wallets"""
    user, pw = create_user()
    clientele = create_oauth_client(user.username, pw)
    clientele.wallets.create(ETHEREUM_ROPSTEN_ASSET_ID, pw)
    wallets = clientele.wallets.all()
    assert isinstance(wallets, list)

def test_list_assets():
    """Tests an API call to list assets"""
    user, pw = create_user()
    clientele = create_oauth_client(user.username, pw)
    assets = clientele.assets.all()
    assert isinstance(assets, list)
    assert assets[0].id == '51bfa4b5-6499-5fe2-998b-5fb3c9403ac7'
    assert assets[0].name == 'Arweave (internal testnet)'
    assert assets[0].symbol == 'AR'
    assert assets[0].exponent == 12
    assert assets[0].protocol == 'arweave_testnet'

def test_send_transaction():
    """Tests an API call to send transactions"""
    user, pw = create_user()
    clientele = create_oauth_client(user.username, pw)
    wallet = clientele.wallets.create(ETHEREUM_ROPSTEN_ASSET_ID,pw)
    transaction =  wallet.transactions.create(
        pw,
        ETHEREUM_ROPSTEN_ASSET_ID,
        10000000000000000,
        41180000000000,
        '0x6720d291a72b8673e774a179434c96d21eb85e71'
    )
    assert transaction.id is not None
    assert transaction.txhash is not None
    assert transaction.sender is not None
    assert transaction.recipient == '0x6720d291a72b8673e774a179434c96d21eb85e71'
    assert transaction.quantity == 10000000000000000
    assert transaction.fee == 41180000000000

def test_list_transactions():
    """Tests an API call to list transactions"""
    clientele = create_oauth_client('alex_test', 'secret')
    wallet = clientele.wallets.all()[0]
    transactions = wallet.transactions.list(8)
    assert len(transactions) == 8

def test_retrieve_transactions():
    """Tests an API call to list transaction"""
    clientele = create_oauth_client('alex_test', 'secret')
    wallet = clientele.wallets.all()[0]
    id = wallet.transactions.all()[0].id
    transaction = wallet.transactions.get(id)
    assert transaction.txhash == '0x029dd84294f4efbc9857a776e2acff0743dec31b8d9e2759872724a80b240e77'

def pubkey_to_ethereum_address(pk):
    kec = sha3.keccak_256(pk.x.to_bytes(32, "big") + pk.y.to_bytes(32, "big")).digest()
    return "0x" + str(hexlify(kec[-20:]), "UTF-8")

def pubkey_to_bitcoin_address(pk, prefix):
    return bitcoin.pubtoaddr(bitcoin.compress((pk.x, pk.y)), magicbyte = prefix)

def test_gpsi_ethereum():
    """Tests an API call to the General Purpose Signing Interface using an Etherum wallet (secp256k1)"""
    user, pw = create_user()
    clientele = create_oauth_client(user.username, pw)
    wallet = clientele.wallets.create(ETHEREUM_ROPSTEN_ASSET_ID, pw)

    message = fresh.bs(1024) # e.g. imagine this is a PDF or a authentication challenge
    signature = wallet.sign(pw, message)

    assert signature.curve == "secp256k1"
    assert hashlib.sha256(message).digest() == signature.signed_hash

    x, y = ecdsa_raw_recover(signature.signed_hash, (27 + signature.recover, signature.r, signature.s))
    assert x == signature.x
    assert y == signature.y
    assert pubkey_to_ethereum_address(signature) == clientele.wallets.get(wallet.id).address

def test_gpsi_bitcoin():
    """Tests an API call to the General Purpose Signing Interface using a Bitcoin wallet (secp256k1)"""
    user, pw = create_user()
    clientele = create_oauth_client(user.username, pw)
    wallet = clientele.wallets.create(BITCOIN_TESTNET_ASSET_ID, pw)

    message = fresh.bs(1024) # e.g. imagine this is a PDF or a authentication challenge
    signature = wallet.sign(pw, message)

    assert signature.curve == "secp256k1"
    assert hashlib.sha256(message).digest() == signature.signed_hash

    x, y = ecdsa_raw_recover(signature.signed_hash, (27 + signature.recover, signature.r, signature.s))
    assert x == signature.x
    assert y == signature.y
    assert pubkey_to_bitcoin_address(signature, prefix=0x6f) == clientele.wallets.get(wallet.id).address
