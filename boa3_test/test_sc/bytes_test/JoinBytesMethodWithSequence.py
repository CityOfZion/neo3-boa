from typing import Sequence

from boa3.builtin.compile_time import public


@public
def main(string: bytes, sequence: Sequence[bytes]) -> bytes:
    return string.join(sequence)
