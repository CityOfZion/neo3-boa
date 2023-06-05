from typing import Union

from boa3.builtin.compile_time import public
from boa3.builtin.type.helper import to_bytes


@public
def example(value: Union[str, int]) -> bytes:
    if isinstance(value, str):
        return to_bytes(value)
    else:
        return to_bytes(value)
