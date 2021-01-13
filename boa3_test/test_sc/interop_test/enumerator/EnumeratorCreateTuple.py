from boa3.builtin import public
from boa3.builtin.interop.enumerator import Enumerator


@public
def tuple_enumerator(x: tuple) -> Enumerator:
    return Enumerator(x)
