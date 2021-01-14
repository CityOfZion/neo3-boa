from boa3.builtin import public
from boa3.builtin.interop.enumerator import Enumerator
from boa3.builtin.interop.storage import find


@public
def find_by_prefix(prefix: int) -> Enumerator:
    return find(prefix)
