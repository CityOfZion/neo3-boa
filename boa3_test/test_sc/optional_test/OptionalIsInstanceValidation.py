from typing import Optional, Union

from boa3.sc.compiletime import public


@public
def main(arg: Optional[str, int]) -> str:
    if isinstance(arg, str):
        return arg
    elif isinstance(arg, int):
        return 'int'
    else:
        return 'None'


@public
def union_test(arg: Optional[Union[str, int]]) -> str:
    if isinstance(arg, str):
        return arg
    elif isinstance(arg, int):
        return 'int'
    else:
        return 'None'
