from typing import Sequence

from boa3.builtin import public


@public
def Main():
    any_list = [True, 1, 'ok']
    int_sequence: Sequence[int] = any_list
