from boa3.builtin import public
from boa3.builtin.interop.contract import update_contract


@public
def update(script: bytes, manifest: bytes):
    update_contract(script, manifest)


@public
def new_method() -> int:
    return 42
