from boa3.builtin import public
from boa3.builtin.interop.enumerator import Enumerator


@public
def int_enumerator(x: int) -> Enumerator:
    return Enumerator(x)
