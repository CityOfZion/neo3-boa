from boa3.builtin import public
from boa3.builtin.interop.storage import get


@public
def Main(key: str) -> bytes:
    return get(key)
