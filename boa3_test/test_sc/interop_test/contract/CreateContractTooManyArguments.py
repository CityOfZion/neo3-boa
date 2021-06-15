from typing import Any

from boa3.builtin.interop.contract import create_contract


def Main(script: bytes, manifest: bytes, data: Any, arg0: Any):
    create_contract(script, manifest, data, arg0)
