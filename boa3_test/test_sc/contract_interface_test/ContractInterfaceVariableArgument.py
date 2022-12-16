from boa3.builtin.compile_time import contract
from boa3.builtin.interop.contract import NEO


@contract(NEO)
class ContractInterface:

    @staticmethod
    def foo():
        pass
