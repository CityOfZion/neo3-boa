from boa3.builtin.compile_time import public
from boa3.builtin.interop.contract import NEO
from boa3.builtin.type import UInt160


@public
def Main(example: UInt160) -> UInt160:
    NEO = example
    return NEO


def interop_call():
    x = NEO
