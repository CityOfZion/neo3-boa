from boa3.sc.compiletime import public
from boa3.sc.contracts import StdLib


@public
def serialize_bool() -> bytes:
    return StdLib.serialize(True)
