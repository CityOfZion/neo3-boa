from boa3.sc.compiletime import public
from boa3.sc.utils import hash160


@public
def Main() -> bytes:
    return hash160(b'unit test')
