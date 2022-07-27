from typing import List

from boa3.builtin import public


@public
def main(x: bytes) -> List[int]:
    return list(x)


def verify_return() -> List[int]:
    return list(b'123')
