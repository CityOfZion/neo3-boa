from boa3.sc.compiletime import public
from boa3.sc.utils import hash160


@public
def Main(test: str) -> bytes:
    return hash160(test)
