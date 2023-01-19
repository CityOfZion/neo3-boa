from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.type import UInt160


@public
def Main(a: Any) -> bool:
    # not supported because boa builtin classes don't work with isinstance yet
    return isinstance(a, (list, int, UInt160, dict))
