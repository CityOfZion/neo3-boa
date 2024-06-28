from typing import Any

from boa3.sc.compiletime import public


@public
def main(x: Any) -> str:
    match x:
        case [1, 2, 3]:
            return "list of 1, 2, 3"
        case [1, 2, x]:
            return f"list of 1, 2, " + x
        case (1, 2):
            return "1 2"
        case (1, "2", x):
            return "1" + "2 string" + x
        case _:
            return "other"
