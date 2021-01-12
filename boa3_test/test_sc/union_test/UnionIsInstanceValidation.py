from typing import Union

from boa3.builtin import public


@public
def main(arg: Union[str, bool]) -> str:
    if isinstance(arg, str):
        return arg
    else:
        return 'boolean'
