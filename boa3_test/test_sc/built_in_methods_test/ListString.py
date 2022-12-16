from typing import List

from boa3.builtin.compile_time import public


@public
def main(x: str) -> List[str]:
    return list(x)
