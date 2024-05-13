from typing import Any

from boa3.sc.compiletime import public


@public
def main() -> Any:
    a = ('unit', 'test')
    return set(a)
