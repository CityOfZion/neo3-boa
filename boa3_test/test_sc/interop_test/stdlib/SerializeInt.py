from boa3.sc.compiletime import public
from boa3.sc.contracts import StdLib


@public
def serialize_int() -> bytes:
    return StdLib.serialize(42)
