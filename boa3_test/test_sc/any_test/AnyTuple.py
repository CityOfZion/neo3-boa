from typing import Any, Tuple

from boa3.builtin.compile_time import public


@public
def Main():
    a: Tuple[Any] = (True, 1, 'ok')
