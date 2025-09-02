from boa3.sc.compiletime import public
from boa3.sc.contracts import LedgerContract
from boa3.sc.types import Block, UInt256, UInt160


def genesis_block() -> Block:
    block = LedgerContract.get_block(0)
    if block is not None:
        return block
    raise Exception("The genesis block should not be None")


@public
def get_hash() -> UInt256:
    return genesis_block().hash


@public
def get_version() -> int:
    return genesis_block().version


@public
def get_previous_hash() -> UInt256:
    return genesis_block().previous_hash


@public
def get_merkle_root() -> UInt256:
    return genesis_block().merkle_root


@public
def get_timestamp() -> int:
    return genesis_block().timestamp


@public
def get_nonce() -> int:
    return genesis_block().nonce


@public
def get_index() -> int:
    return genesis_block().index


@public
def get_primary_index() -> int:
    return genesis_block().primary_index


@public
def get_next_consensus() -> UInt160:
    return genesis_block().next_consensus


@public
def get_transaction_count() -> int:
    return genesis_block().transaction_count
