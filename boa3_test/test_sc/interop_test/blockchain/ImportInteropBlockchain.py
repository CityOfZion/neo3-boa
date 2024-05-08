from boa3.builtin import interop, type
from boa3.builtin.compile_time import public


@public
def main(hash_: type.UInt160) -> interop.contract.Contract | None:
    return interop.blockchain.get_contract(hash_)
