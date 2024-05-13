from collections.abc import Sequence

from boa3.sc.compiletime import public


@public
def main(string: str, sequence: Sequence[str]) -> str:
    return string.join(sequence)
