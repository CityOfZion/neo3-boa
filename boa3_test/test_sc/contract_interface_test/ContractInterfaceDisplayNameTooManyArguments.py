from boa3.sc.compiletime import contract, display_name


@contract('0x0102030405060708090A0B0C0D0E0F1011121314')
class ContractInterface:

    @staticmethod
    @display_name('someMethod', 'anotherArgument')
    def foo():
        pass
