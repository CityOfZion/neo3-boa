from typing import cast

from boa3.builtin import public
from boa3.builtin.interop.contract import call_contract
from boa3.builtin.type import UInt160


@public
def Main(scripthash: bytes, method: str, args: list) -> bool:
    call_contract(cast(UInt160, scripthash), method, args)
    return True
