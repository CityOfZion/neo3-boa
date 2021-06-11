from typing import Any

from boa3.builtin import interop, public, type


@public
def call_flags_all() -> interop.contract.CallFlags:
    return interop.contract.CallFlags.ALL


@public
def main(scripthash: type.UInt160, method: str, args: list) -> Any:
    return interop.contract.call_contract(scripthash, method, args)
