from boa3.builtin.compile_time import contract
from boa3.builtin.type import UInt160
from boa3.sc.compiletime import public


@contract("0x0123456789abcdef0123456789abcdef01234567")
class Example:
    hash: UInt160

    @staticmethod
    def total() -> int:
        pass


class ExampleStaticVars:
    value1 = 1
    value2 = 2


@public
def main() -> int:
    return ExampleStaticVars.value1
