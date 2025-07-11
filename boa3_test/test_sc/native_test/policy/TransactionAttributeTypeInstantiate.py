from boa3.sc.compiletime import public
from boa3.sc.types import TransactionAttributeType


@public
def main(x: int) -> TransactionAttributeType:
    return TransactionAttributeType(x)
