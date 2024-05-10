from boa3.builtin.compile_time import public
from boa3.builtin.type.helper import to_bytes
from boa3.sc import storage


@public
def int_to_bytes(value: int):
    Example(value)


def return_bytes(value: bytes) -> bytes:
    return value


class Example:
    def __init__(self, current_supply: int):

        set_value(to_bytes(current_supply), self)


def set_value(token_id: bytes, example_class: Example):
    storage.put_object(b'00' + token_id, example_class)
