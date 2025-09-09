from boa3.sc.compiletime import contract
from boa3.sc.types import UInt160

test = UInt160()


@contract(test)
class ContractInterface:

    @staticmethod
    def foo():
        pass
