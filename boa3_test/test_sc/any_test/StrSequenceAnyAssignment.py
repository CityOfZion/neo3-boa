from typing import Sequence

from boa3.builtin.compile_time import public


@public
def Main():
    any_tuple = (True, 1, 'ok')
    str_sequence: Sequence[str] = any_tuple
