from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.stdlib import StdLib


@public
def deserialize_arg(arg: bytes) -> Any:
    return StdLib.deserialize(arg)
