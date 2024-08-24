from boa3.builtin.interop import blockchain
from boa3.sc.compiletime import public
from boa3.sc.types import UInt160, Contract


@public
def main(hash_: UInt160) -> Contract | None:
    return blockchain.get_contract(hash_)
