from typing import Union

from boa3.sc.compiletime import public


@public
def Main():
    a = 2
    b: Union[int, list] = a
    c = [a, b]
    b = c
