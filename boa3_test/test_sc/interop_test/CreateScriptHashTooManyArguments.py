from typing import Any
from boa3.builtin.interop.contract import create_contract


def Main(script: bytes, manifest: bytes, arg0: Any):
    create_contract(script, manifest, arg0)

