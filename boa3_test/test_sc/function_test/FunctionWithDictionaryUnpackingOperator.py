from typing import Any

from boa3.builtin.compile_time import public


@public
def function_with_unpacking(**kwargs: dict[Any, Any]) -> int:  # not sure if Dict is the best type
    return len(kwargs)


@public
def main(dictionary: dict[str, int]) -> int:
    return function_with_unpacking(**dictionary)
