from boa3.sc.compiletime import contract


@contract('0x0102030405060708090A0B0C0D0E0F1011121314', '123')
class ContractInterface:

    @staticmethod
    def foo():
        pass
