from boa3.sc.compiletime import public
from boa3.sc.storage import find


@public
def dict_iterator(prefix: str) -> str:
    it = find(prefix)
    it.next()
    return it.value  # 'find' Iterator value is str | bytes
