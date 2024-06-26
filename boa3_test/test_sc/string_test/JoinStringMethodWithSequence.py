from collections.abc import Sequence

from boa3.builtin.compile_time import public


@public
def main(string: str, sequence: Sequence[str]) -> str:
    return string.join(sequence)
