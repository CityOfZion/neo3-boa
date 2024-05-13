from typing import Any

from boa3.sc.compiletime import public


@public
def main(a: Any) -> str:
    fstring = f"F-string: {a}"
    return fstring
