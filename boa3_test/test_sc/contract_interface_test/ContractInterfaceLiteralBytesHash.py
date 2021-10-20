from boa3.builtin import contract


@contract(b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F\x10\x11\x12\x13\x14')
class ContractInterface:

    @staticmethod
    def foo():
        pass
