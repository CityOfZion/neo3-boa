from boa3.builtin.compile_time import public
from boa3.builtin.interop.storage import find


@public
def has_next(prefix: str) -> bool:
    return find(prefix).next()
