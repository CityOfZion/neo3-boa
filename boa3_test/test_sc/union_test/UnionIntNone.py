from typing import Union

from boa3.builtin import public


@public
def main() -> Union[int, None]:
    x: Union[int, None] = None
    x = 42
    return x
