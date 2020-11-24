from boa3.builtin import public
from boa3.builtin.interop.contract import create_contract, Contract


@public
def Main(script: bytes, manifest: bytes) -> Contract:
    return create_contract(script, manifest)
