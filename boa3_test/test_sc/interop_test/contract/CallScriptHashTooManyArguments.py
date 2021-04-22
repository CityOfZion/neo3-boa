from typing import Any

from boa3.builtin.interop.contract import call_contract, CallFlags


def Main(scripthash: bytes, method: str, arg0: Any, arg1: Any, flags: CallFlags):
    call_contract(scripthash, method, arg0, arg1, flags)
