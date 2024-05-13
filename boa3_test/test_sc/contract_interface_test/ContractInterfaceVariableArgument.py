from boa3.builtin.interop.contract import NEO
from boa3.sc.compiletime import contract


@contract(NEO)
class ContractInterface:

    @staticmethod
    def foo():
        pass
