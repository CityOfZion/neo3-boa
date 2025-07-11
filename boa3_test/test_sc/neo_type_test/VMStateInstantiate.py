from boa3.sc.compiletime import public
from boa3.sc.types import VMState


@public
def main(x: int) -> VMState:
    return VMState(x)
