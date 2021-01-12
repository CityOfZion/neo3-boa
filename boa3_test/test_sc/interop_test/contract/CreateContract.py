from boa3.builtin import public
from boa3.builtin.interop.contract import Contract, create_contract


@public
def Main(script: bytes, manifest: bytes) -> Contract:
    return create_contract(script, manifest)
