from boa3.sc.compiletime import contract, public
from boa3.sc.types import UInt160


@contract('0x000102030405060708090A0B0C0D0E0F10111213')
class ContractInterface:
    hash: UInt160

    @staticmethod
    def foo():
        pass


@public
def main() -> UInt160:
    return ContractInterface.hash
