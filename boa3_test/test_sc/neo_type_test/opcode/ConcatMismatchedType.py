from boa3.sc.compiletime import public
from boa3.sc.types import Opcode


@public
def concat(arg: Opcode) -> str:
    return '12345' + arg
