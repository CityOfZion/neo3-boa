from typing import Optional, Union

from boa3.builtin.compile_time import public


@public
def main(return_type: int) -> Optional[str, int]:
    if return_type == 1:
        return 'str'
    elif return_type == 2:
        return 123
    else:
        return None


@public
def union_test(return_type: int) -> Optional[Union[str, int]]:
    if return_type == 1:
        return 'str'
    elif return_type == 2:
        return 123
    else:
        return None
