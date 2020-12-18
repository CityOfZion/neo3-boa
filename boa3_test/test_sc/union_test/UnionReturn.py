from typing import Union

from boa3.builtin import public


@public
def main(return_int: bool) -> Union[int, str]:
    if return_int:
        return 42
    else:
        return '42'
