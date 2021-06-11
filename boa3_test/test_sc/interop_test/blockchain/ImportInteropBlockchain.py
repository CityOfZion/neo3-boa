from boa3.builtin import interop, public, type


@public
def main(hash_: type.UInt160) -> interop.contract.Contract:
    return interop.blockchain.get_contract(hash_)
