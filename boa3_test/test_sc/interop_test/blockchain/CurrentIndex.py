from boa3.sc.compiletime import public
from boa3.sc.contracts import LedgerContract


@public
def main() -> int:
    return LedgerContract.get_current_index()
