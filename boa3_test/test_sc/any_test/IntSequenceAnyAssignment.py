from collections.abc import Sequence

from boa3.sc.compiletime import public


@public
def Main():
    any_list = [True, 1, 'ok']
    int_sequence: Sequence[int] = any_list
