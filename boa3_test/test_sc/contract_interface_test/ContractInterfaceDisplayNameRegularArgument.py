from boa3.builtin import contract, display_name, public


@contract('0x0102030405060708090A0B0C0D0E0F1011121314')
class ContractInterface:

    @staticmethod
    @display_name('someMethod')
    def foo():
        pass


@public
def main():
    ContractInterface.foo()
