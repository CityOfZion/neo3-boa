from typing import Any

from boa3.builtin import public
from boa3.builtin.interop import contract
from boa3.builtin.type import UInt160


@public
def call_flags_all() -> contract.CallFlags:
    return contract.CallFlags.ALL


@public
def main(scripthash: UInt160, method: str, args: list) -> Any:
    return contract.call_contract(scripthash, method, args)
