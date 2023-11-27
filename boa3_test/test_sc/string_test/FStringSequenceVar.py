from typing import List

from boa3.builtin.compile_time import public


@public
def main(a: List) -> str:
    fstring = f"F-string: {a}"
    return fstring
