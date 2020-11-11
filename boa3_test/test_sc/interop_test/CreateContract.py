from typing import Any

from boa3.builtin import public
from boa3.builtin.interop.contract import create_contract


@public
def Main(script: bytes, manifest: bytes) -> Any:
    return create_contract(script, manifest)
