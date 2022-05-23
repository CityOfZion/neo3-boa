from boa3.builtin.interop import storage

from boa3.builtin import public
from boa3.builtin.interop.stdlib import serialize


@public
def int_to_bytes(value: int):
    Example(value)


def return_bytes(value: bytes) -> bytes:
    return value


class Example:
    def __init__(self, current_supply: int):

        set_value(current_supply.to_bytes(), self)


def set_value(token_id: bytes, example_class: Example):
    storage.put(b'00' + token_id, serialize(example_class))
