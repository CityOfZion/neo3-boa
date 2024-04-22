from typing import Union

from boa3.builtin.compile_time import public


@public
def main(x: Union[bytes, str]) -> list[Union[int, str]]:
    a = 'unit test'
    b = b'unit test'

    return list(x)
