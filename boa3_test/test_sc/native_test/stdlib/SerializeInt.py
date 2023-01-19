from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.stdlib import StdLib


@public
def serialize_int() -> bytes:
    return StdLib.serialize(42)
