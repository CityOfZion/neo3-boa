from typing import Any

from boa3.builtin.compile_time import public


@public
def Main():
    a: tuple[Any, Any, Any] = (True, 1, 'ok')
