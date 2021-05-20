from boa3.builtin import public
from boa3.builtin.interop.blockchain import get_transaction_from_block, Transaction


@public
def main(height: int, tx_index: int) -> Transaction:
    return get_transaction_from_block(height, tx_index)
