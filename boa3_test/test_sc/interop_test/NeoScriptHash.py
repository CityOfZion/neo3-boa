from boa3.builtin import public
from boa3.builtin.interop.contract import NEO


@public
def Main() -> bytes:
    return NEO
