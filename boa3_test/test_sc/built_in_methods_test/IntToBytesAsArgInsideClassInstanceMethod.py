from boa3.sc.compiletime import public
from boa3.sc.utils import to_bytes


class Example:
    def __init__(self):
        self.prop1 = b''
        self.prop2 = b''
        self.set_property1(
            to_bytes(30)
        )
        self.set_property2(
            to_bytes(10), to_bytes(20)
        )

    def set_property1(self, param: bytes):
        self.prop1 = param

    def set_property2(self, param1: bytes, param2: bytes):
        self.prop2 = param1 + param2


@public
def int_to_bytes() -> bytes:
    test = Example()
    return test.prop1


@public
def int_to_bytes2() -> bytes:
    test = Example()
    return test.prop2
