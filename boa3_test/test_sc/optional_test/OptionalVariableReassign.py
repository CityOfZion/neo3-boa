from typing import Optional

from boa3.builtin import public


@public
def Main():
    a = 2
    b: Optional[int] = a
    c = None
    b = c
