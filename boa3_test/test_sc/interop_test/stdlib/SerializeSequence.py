from boa3.sc.compiletime import public
from boa3.sc.contracts import StdLib


@public
def serialize_sequence() -> bytes:
    return StdLib.serialize([2, 3, 5, 7])
