from typing import Sequence

from boa3.builtin.compile_time import public


@public
def Main():
    int_list = [1, 2, 3]
    int_tuple = 10, 9, 8

    a: Sequence[Sequence[int]] = [int_list, int_tuple]
