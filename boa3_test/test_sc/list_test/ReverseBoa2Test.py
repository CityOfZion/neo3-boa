from typing import Any

from boa3.sc.compiletime import public


@public
def main() -> list[Any]:
    m = [1, 2, 4, 'blah']
    m.reverse()
    return m
