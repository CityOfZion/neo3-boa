from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.storage import get_int, put_int

key = b'1'

@public
def main() -> int:
    return get_int(key)


@public
def _deploy(data: Any, update: bool):
    variable = 1
    variable = 123
    put_int(key, variable)
    return None
