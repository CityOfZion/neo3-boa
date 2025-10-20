from typing import Any

from boa3.sc.compiletime import public

key = b'1'
global_var = 'original'


@public
def main() -> str:
    return global_var


@public
def _deploy(data: Any, update: bool):
    global global_var
    global_var = 'change'
    return None
