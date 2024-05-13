from boa3.sc.compiletime import public
from boa3.sc.utils import hash256


@public
def Main() -> bytes:
    return hash256(b'unit test')
