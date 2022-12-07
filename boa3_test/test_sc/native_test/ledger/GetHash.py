from boa3.builtin import public
from boa3.builtin.nativecontract.ledger import Ledger
from boa3.builtin.type import UInt160


@public
def main() -> UInt160:
    return Ledger.hash
