from boa3.builtin.compile_time import NeoMetadata, contract, public
from boa3.builtin.type import UInt160


@contract('0x000102030405060708090A0B0C0D0E0F10111213')
class ContractInterface:
    hash: UInt160

    @staticmethod
    def foo():
        pass


def contract_metadata() -> NeoMetadata:
    obj = NeoMetadata()
    obj.add_permission(contract=ContractInterface.hash)
    return obj


@public
def main() -> UInt160:
    return ContractInterface.hash
