from boa3.builtin import public
from boa3.builtin.interop.enumerator import Enumerator


@public
def concat_enumerators(x: list, y: list) -> Enumerator:
    it1 = Enumerator(x)
    it2 = Enumerator(y)

    return it1.concat(it2)
