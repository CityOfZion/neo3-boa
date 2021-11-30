from boa3.builtin import public
from boa3.builtin.nativecontract.ledger import Ledger


@public
def main() -> int:
    return Ledger.get_current_index()
