from boa3.builtin import public
from boa3.builtin.interop.enumerator import Enumerator


@public
def list_enumerator(x: list) -> Enumerator:
    return Enumerator(x)
