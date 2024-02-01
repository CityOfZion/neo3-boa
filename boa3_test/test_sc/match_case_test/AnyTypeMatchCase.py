from typing import Any

from boa3.builtin.compile_time import public


@public
def main(x: Any) -> str:
    match x:
        case True:
            return "True"
        case 1:
            return "one"
        case "2":
            return "2 string"
        case _:
            # this is the default case, when all others are False
            return "other"
