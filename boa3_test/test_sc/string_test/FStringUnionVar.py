from typing import Union

from boa3.builtin.compile_time import public


@public
def main(a: Union[int, str]) -> str:
    fstring = f"F-string: {a}"
    return fstring
