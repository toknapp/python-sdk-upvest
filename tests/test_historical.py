from .partials.client_instance import create_tenancy_client

ETH_PROTOCOL = "ethereum"
ETH_ROPSTEN_NETWORK = "ropsten"

tenancy = create_tenancy_client()


def test_get_transactions_by_txhash():
    txhash = "0xa313aaad0b9b1fd356f7f42ccff1fa385a2f7c2585e0cf1e0fb6814d8bdb559a"
    tx = tenancy.historical.get_transaction(ETH_PROTOCOL, ETH_ROPSTEN_NETWORK, txhash)
    assert tx.hash == txhash[2:]


def test_get_transactions_by_address():
    from functools import partial

    to_addr = "0x6590896988376a90326cb2f741cb4f8ace1882d5"
    func = partial(tenancy.historical.get_transactions, ETH_PROTOCOL, ETH_ROPSTEN_NETWORK, to_addr)
    # before & after
    before, after = 6_613_892, 6_613_887
    filters = dict(before=before, after=after)
    txs = func(filters)
    assert all([(int(x.blockNumber) >= after) and (int(x.blockNumber) <= before) for x in txs.result])

    # min confirmations
    confirmations = 1000
    filters = dict(confirmations=confirmations)
    txs = func(filters)
    assert all([(int(x.confirmations) > confirmations) for x in txs.result])

    # retrieve all txs by address
    txs = func()
    assert isinstance(txs.result, list)


def test_get_block():
    block = tenancy.historical.get_block(ETH_PROTOCOL, ETH_ROPSTEN_NETWORK, "latest")
    assert block.number is not None
    # int
    block_number = "6570890"
    block = tenancy.historical.get_block(ETH_PROTOCOL, ETH_ROPSTEN_NETWORK, block_number)
    assert block.number == block_number


def test_get_asset_balance():
    to_addr = "0x93b3d0b2894e99c2934bed8586ea4e2b94ce6bfd"
    balance = tenancy.historical.get_asset_balance(ETH_PROTOCOL, ETH_ROPSTEN_NETWORK, to_addr)
    assert balance.address
    assert balance.contract is None
    assert balance.address == to_addr


def test_get_contract_balance():
    to_addr = "0x93b3d0b2894e99c2934bed8586ea4e2b94ce6bfd"
    contract_addr = "0x1d7cf6ad190772cc6177beea2e3ae24cc89b2a10"
    balance = tenancy.historical.get_contract_balance(ETH_PROTOCOL, ETH_ROPSTEN_NETWORK, to_addr, contract_addr)
    assert balance.address
    assert balance.address == to_addr
    assert balance.contract == contract_addr


def test_status():
    status = tenancy.historical.get_api_status(ETH_PROTOCOL, ETH_ROPSTEN_NETWORK)
    assert all((status.lowest, status.highest, status.latest))
