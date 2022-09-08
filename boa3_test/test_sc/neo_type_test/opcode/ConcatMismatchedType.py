from boa3.builtin import public
from boa3.builtin.vm import Opcode


@public
def concat(arg: Opcode) -> str:
    return '12345' + arg
