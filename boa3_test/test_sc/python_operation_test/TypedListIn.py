from typing import List

from boa3.builtin.compile_time import public


@public
def main(value: int, some_list: List[int]) -> bool:
    return value in some_list
