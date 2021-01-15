from boa3.builtin import public
from boa3.builtin.interop.enumerator import Enumerator


@public
def concat_enumerators(x: list) -> Enumerator:
    it1 = Enumerator(x)

    return it1.concat(42)
