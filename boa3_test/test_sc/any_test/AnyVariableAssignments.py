from typing import Any

from boa3.sc.compiletime import public


@public
def Main():
    a: Any = 1
    a = '2'
    a = True
    a = [1, 2, 3]
