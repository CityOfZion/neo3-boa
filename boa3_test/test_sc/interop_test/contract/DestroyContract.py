from boa3.builtin import public
from boa3.builtin.interop.contract import destroy_contract


@public
def Main():
    destroy_contract()
