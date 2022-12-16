from typing import List

from boa3.builtin.compile_time import public


@public
def create_bytearray(int_list: List[int]) -> bytearray:
    return bytearray(int_list)  # not supported yet
