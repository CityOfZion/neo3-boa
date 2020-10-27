from typing import Dict

from boa3.builtin import public


@public
def Main(a: Dict[int, str]) -> Dict[int, str]:
    a[0] = 'ok'
    return a
