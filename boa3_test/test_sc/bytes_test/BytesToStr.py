from boa3.sc.compiletime import public
from boa3.sc.utils import to_str


@public
def bytes_to_str() -> str:
    return to_str(b'abc')
