from boa3.builtin import public
from boa3.builtin.interop.blockchain import get_contract
from boa3.builtin.interop.contract import Contract


@public
def main(hash: bytes) -> Contract:
    return get_contract(hash)
