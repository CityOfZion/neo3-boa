from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.storage import put_str, get_str

key = b'1'
shadow = 'shadow'


@public
def main() -> str:
    return get_str(key)


@public
def get_global_var() -> str:
    return shadow


@public
def _deploy(data: Any, update: bool):
    shadow = 'new variable'
    put_str(key, shadow)
    return None
