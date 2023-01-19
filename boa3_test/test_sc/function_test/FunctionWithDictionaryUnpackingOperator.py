from typing import Any, Dict

from boa3.builtin.compile_time import public


@public
def function_with_unpacking(**kwargs: Dict[Any, Any]) -> int:  # not sure if Dict is the best type
    return len(kwargs)


@public
def main(dictionary: Dict[str, int]) -> int:
    return function_with_unpacking(**dictionary)
