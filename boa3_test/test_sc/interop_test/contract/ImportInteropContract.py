from typing import Any

from boa3.builtin import interop, type
from boa3.builtin.compile_time import public


@public
def call_flags_all() -> interop.contract.CallFlags:
    return interop.contract.CallFlags.ALL


@public
def main(scripthash: type.UInt160, method: str, args: list) -> Any:
    return interop.contract.call_contract(scripthash, method, args)
