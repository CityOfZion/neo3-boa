from typing import List

from boa3.builtin import public


@public
def main(x: str) -> List[str]:
    return list(x)
