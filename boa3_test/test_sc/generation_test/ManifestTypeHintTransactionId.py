from boa3.builtin.compile_time import public
from boa3.builtin.type import TransactionId, UInt256


@public
def main() -> TransactionId:
    return TransactionId(UInt256())
