from boa3.builtin import contract, public
from boa3.builtin.type import UInt160


@contract('0x000102030405060708090A0B0C0D0E0F10111213')
class ContractInterface:

    @staticmethod
    def foo():
        pass


@public
def main() -> UInt160:
    return ContractInterface.hash
