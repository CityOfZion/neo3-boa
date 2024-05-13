from collections.abc import Sequence

from boa3.sc.compiletime import public


@public
def Main():
    int_list = [1, 2, 3]
    int_tuple = 10, 9, 8

    a: Sequence[Sequence[int]] = [int_list, int_tuple]
