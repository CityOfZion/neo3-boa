from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop.stdlib import deserialize


@public
def deserialize_arg() -> Any:
    return deserialize(1)
