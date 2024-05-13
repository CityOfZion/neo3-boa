from boa3.sc.compiletime import public
from boa3.sc.contracts import StdLib


@public
def serialize_dict() -> bytes:
    return StdLib.serialize({1: 1, 2: 1, 3: 2})
