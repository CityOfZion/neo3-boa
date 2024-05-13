from collections.abc import Sequence

from boa3.sc.compiletime import public


@public
def main(string: bytes, sequence: Sequence[bytes]) -> bytes:
    return string.join(sequence)
