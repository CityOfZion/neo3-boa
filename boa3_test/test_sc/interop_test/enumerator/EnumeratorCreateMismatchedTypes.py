from boa3.builtin import public
from boa3.builtin.interop.enumerator import Enumerator


@public
def dict_enumerator(x: dict) -> Enumerator:
    return Enumerator(x)
