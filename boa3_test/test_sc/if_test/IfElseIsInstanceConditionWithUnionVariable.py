from typing import Union

from boa3.builtin import public


@public
def example(value: Union[str, int]) -> bytes:
    if isinstance(value, int):
        return value.to_bytes()
    else:
        return value.to_bytes()
