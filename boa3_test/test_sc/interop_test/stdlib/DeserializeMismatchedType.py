from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.contracts import StdLib


@public
def deserialize_arg() -> Any:
    return StdLib.deserialize(1)
