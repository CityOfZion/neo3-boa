from boa3.builtin import public
from boa3.builtin.interop import blockchain
from boa3.builtin.interop.contract import Contract
from boa3.builtin.type import UInt160


@public
def main(hash_: UInt160) -> Contract:
    return blockchain.get_contract(hash_)
