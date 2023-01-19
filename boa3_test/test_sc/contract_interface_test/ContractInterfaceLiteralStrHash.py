from boa3.builtin.compile_time import contract, public


@contract('0x0102030405060708090A0B0C0D0E0F1011121314')
class ContractInterface:

    @staticmethod
    def foo():
        pass


@public
def main():
    ContractInterface.foo()
