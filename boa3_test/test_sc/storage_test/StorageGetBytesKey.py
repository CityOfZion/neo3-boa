from boa3.sc.compiletime import public
from boa3.sc.storage import get


@public
def Main(key: bytes) -> bytes:
    return get(key)
