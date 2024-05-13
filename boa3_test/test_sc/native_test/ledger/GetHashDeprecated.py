from boa3.sc.compiletime import public
from boa3.builtin.nativecontract.ledger import Ledger
from boa3.sc.types import UInt160


@public
def main() -> UInt160:
    return Ledger.hash
