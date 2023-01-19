from typing import Any

from boa3.builtin.compile_time import public


@public
def main(value: Any, some_list: list) -> bool:
    return value not in some_list
