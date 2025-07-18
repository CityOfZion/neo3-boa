from boa3.sc.compiletime import public
from boa3.sc.types import TransactionAttributeType


@public
def main(x: TransactionAttributeType) -> int:
    return ~x
