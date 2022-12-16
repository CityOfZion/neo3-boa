from typing import List

from boa3.builtin.compile_time import public


@public
def main(string: str) -> List[str]:
    return string.split()
