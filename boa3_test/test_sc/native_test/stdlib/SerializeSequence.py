from boa3.builtin import public
from boa3.builtin.nativecontract.stdlib import StdLib


@public
def serialize_sequence() -> bytes:
    return StdLib.serialize([2, 3, 5, 7])
