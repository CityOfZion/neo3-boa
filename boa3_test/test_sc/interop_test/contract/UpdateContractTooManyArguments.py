from typing import Any

from boa3.builtin.interop.contract import update_contract


def Main(script: bytes, manifest: str, arg0: Any):
    update_contract(script, manifest, arg0)
