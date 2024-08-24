from boa3.sc.compiletime import public
from boa3.sc.utils import hash256


@public
def Main(test: str) -> bytes:
    return hash256(test)
