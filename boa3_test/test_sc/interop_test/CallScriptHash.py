from typing import Any

from boa3.builtin import public
from boa3.builtin.interop.contract import call_contract


@public
def Main(scripthash: bytes, method: str, args: list) -> Any:
    return call_contract(scripthash, method, args)
