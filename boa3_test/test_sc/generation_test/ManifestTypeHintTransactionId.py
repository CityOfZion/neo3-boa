from boa3.sc.compiletime import public
from boa3.sc.types import UInt256, TransactionId


@public
def main() -> TransactionId:
    return TransactionId(UInt256())
