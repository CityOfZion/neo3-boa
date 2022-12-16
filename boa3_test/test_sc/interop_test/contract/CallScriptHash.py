from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop.contract import call_contract
from boa3.builtin.type import UInt160


@public
def Main(scripthash: UInt160, method: str, args: list) -> Any:
    return call_contract(scripthash, method, args)
