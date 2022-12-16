from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop.contract import Contract, create_contract


@public
def Main(script: bytes, manifest: bytes, data: Any) -> Contract:
    return create_contract(script, manifest, data)
