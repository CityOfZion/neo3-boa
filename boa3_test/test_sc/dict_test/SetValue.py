from typing import Dict

from boa3.builtin.compile_time import public


@public
def Main(a: Dict[int, str]) -> Dict[int, str]:
    a[0] = 'ok'
    return a
