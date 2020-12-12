from boa3.builtin import public
from boa3.builtin.interop.contract import Contract


@public
def new_contract() -> Contract:
    return Contract()
