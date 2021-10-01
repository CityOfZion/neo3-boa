from typing import Sequence

from boa3.builtin import public


@public
def main(string: str, sequence: Sequence[str]) -> str:
    return string.join(sequence)
