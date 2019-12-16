"""Historical data objects"""
from collections import namedtuple

HDBlock = namedtuple(
    "HDBlock",
    [
        "number",
        "hash",
        "parentHash",
        "nonce",
        "sha3Uncles",
        "logsBloom",
        "transactionsRoot",
        "stateRoot",
        "receiptsRoot",
        "miner",
        "difficulty",
        "totalDifficulty",
        "extraData",
        "size",
        "gasLimit",
        "gasUsed",
        "transactions",
        "timestamp",
        "uncles",
    ],
)

HDTransaction = namedtuple(
    "HDTransaction",
    [
        "blockHash",
        "blockNumber",
        # replace "from" with "sender" to suppress Python error on keyword
        "sender",
        "gasLimit",
        "hash",
        "nonce",
        "transactionIndex",
        "to",
        "value",
        "gasPrice",
        "input",
        "confirmations",
    ],
)

# if native asset balance,contract is set to address of the contract
HDBalance = namedtuple(
    "HDBalance",
    [
        "id",
        "address",
        "contract",
        "balance",
        "transactionHash",
        "transactionIndex",
        "blockHash",
        "blockNumber",
        "timestamp",
        "isMainChain",
    ],
)

# result is a list of HDTransaction objects
HDTransactions = namedtuple("HDTransactions", ["result", "next_cursor"])

HDStatus = namedtuple("HDStatus", ["lowest", "highest", "latest"])
