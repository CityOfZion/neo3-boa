from boa3.builtin.compile_time import contract


@contract('0x010203')
class ContractInterface:

    @staticmethod
    def foo():
        pass
