from typing import Any

from boa3.builtin.compile_time import public


@public
def main(param: Any) -> Any:
    other = param or "some default value"
    return other
