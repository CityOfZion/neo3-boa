from boa3.sc.compiletime import public
from boa3.sc.types import VMState


@public
def main(x: VMState) -> int:
    return ~x
