from collections.abc import Sequence

from boa3.sc.compiletime import public


@public
def Main():
    any_tuple = (True, 1, 'ok')
    str_sequence: Sequence[str] = any_tuple
