from typing import cast

from boa3.builtin.compile_time import public
from boa3.builtin.interop.stdlib import deserialize, serialize


class Example:
    def __init__(self):
        self.val1 = 2
        self.val2 = self.val1 * 2

    def some_method(self) -> int:
        return 42


@public
def serialize_user_class() -> bytes:
    user_class = Example()
    return serialize(user_class)


@public
def deserialize_user_class(arg: bytes) -> Example:
    user_class = cast(Example, deserialize(arg))
    return user_class


@public
def get_variable_from_deserialized(arg: bytes) -> int:
    user_class = deserialize_user_class(arg)
    return user_class.val1


@public
def call_method_from_deserialized(arg: bytes) -> int:
    user_class = deserialize_user_class(arg)
    return user_class.some_method()
