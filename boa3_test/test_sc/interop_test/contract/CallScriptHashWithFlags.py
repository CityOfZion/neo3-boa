from typing import Any

from boa3.builtin import public
from boa3.builtin.interop.contract import call_contract, CallFlags
from boa3.builtin.type import UInt160


@public
def Main(scripthash: UInt160, method: str, args: list, flags: CallFlags) -> Any:
    return call_contract(scripthash, method, args, flags)
