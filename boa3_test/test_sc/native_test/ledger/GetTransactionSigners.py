from boa3.builtin import public
from boa3.builtin.nativecontract.ledger import Ledger
from boa3.builtin.type import UInt256


@public
def main(hash_: UInt256) -> list:
    return Ledger.get_transaction_signers(hash_)
