from boa3.builtin import public
from boa3.builtin.nativecontract.stdlib import StdLib


@public
def serialize_dict() -> bytes:
    return StdLib.serialize({1: 1, 2: 1, 3: 2})
