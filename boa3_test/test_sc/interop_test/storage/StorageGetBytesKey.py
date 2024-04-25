from boa3.builtin.compile_time import public
from boa3.sc.storage import get


@public
def Main(key: bytes) -> bytes:
    return get(key)
