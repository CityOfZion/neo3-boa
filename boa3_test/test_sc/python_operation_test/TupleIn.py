from typing import Any

from boa3.builtin import public


@public
def main(value: Any, some_tuple: tuple) -> bool:
    return value in some_tuple
