from typing import Any

from boa3.builtin.compile_time import public


@public
def main(value: Any, some_tuple: tuple) -> bool:
    return value not in some_tuple
