"""Historical data objects"""
import collections


def namedtuple(typename, field_names):
    """
    Creates a namedtuple object that silently ignores unknown keys.

    This ensures compatibility with changing API.
    """
    base = collections.namedtuple("Base", field_names)
    return type(
        typename,
        (base,),
        {
            "__slots__": (),
            "__new__": lambda cls, *args, **kwargs: base.__new__(
                cls, *args, **{k: v for k, v in kwargs.items() if k in base._fields}
            ),
        },
    )


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
        "error",
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
