from typing import Any

from boa3.builtin.compile_time import contract, display_name
from boa3.builtin.type import UInt160


@contract('0x1234567890123456789012345678901234567890')
class ExternalContract:

    @staticmethod
    def method1(arg1: bytes, arg2: UInt160, arg3: Any) -> UInt160:
        pass

    @staticmethod
    @display_name("anotherMethod")
    def another_method() -> str:
        pass

    @staticmethod
    @display_name("onNEP17Payment")
    def on_nep_17_payment(from_address: UInt160, amount: int, data: Any) -> None:
        pass
