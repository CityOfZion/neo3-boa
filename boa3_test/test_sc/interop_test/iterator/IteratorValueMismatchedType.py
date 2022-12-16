from boa3.builtin.compile_time import public
from boa3.builtin.interop.storage import find


@public
def dict_iterator(prefix: str) -> str:
    it = find(prefix)
    it.next()
    return it.value  # 'find' Iterator value is Union[str, bytes]
