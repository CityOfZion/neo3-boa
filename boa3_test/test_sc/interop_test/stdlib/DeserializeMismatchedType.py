from typing import Any

from boa3.builtin import public
from boa3.builtin.interop.stdlib import deserialize


@public
def deserialize_arg() -> Any:
    return deserialize(1)
