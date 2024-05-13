from boa3.sc.compiletime import public
from boa3.sc.utils import to_bool


@public
def bytes_to_bool(args: bytes) -> bool:
    return to_bool(args)
