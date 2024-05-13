from boa3.builtin.interop.storage import get
from boa3.sc.compiletime import public


@public
def Main(key: bytes) -> bytes:
    return get(key)
