from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.contracts import StdLib


@public
def deserialize_arg(arg: bytes) -> Any:
    return StdLib.deserialize(arg)
