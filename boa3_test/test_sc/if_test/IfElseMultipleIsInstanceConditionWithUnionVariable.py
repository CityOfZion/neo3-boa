from typing import List, Union

from boa3.builtin.compile_time import public


@public
def example(value: Union[List[bytes], int, bytes]) -> int:
    if isinstance(value, (list, bytes)):
        x = value if isinstance(value, bytes) else (b'\x00' if len(value) == 0 else value[0])
        return len(x)
    else:
        return value * value
