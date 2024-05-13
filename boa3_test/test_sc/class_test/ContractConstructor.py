from boa3.sc.compiletime import public
from boa3.sc.types import Contract


@public
def new_contract() -> Contract:
    return Contract()
