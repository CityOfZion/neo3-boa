from typing import Union

from boa3.builtin import public


@public
def Main():
    a = 2
    b: Union[int, list] = a
    c = [a, b]
    b = c
