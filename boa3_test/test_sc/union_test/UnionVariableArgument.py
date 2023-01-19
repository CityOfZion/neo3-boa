from typing import Union

from boa3.builtin.compile_time import public


@public
def main(arg: Union[str, bool]) -> str:
    if isinstance(arg, str):
        return 'string'
    else:
        return 'boolean'
