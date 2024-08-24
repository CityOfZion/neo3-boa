from typing import Any

from boa3.sc.compiletime import public


@public
def main(x: Any) -> str:
    match x:
        case True:
            return "True"
        case 1:
            return "one"
        case "2":
            return "2 string"
        case {}:
            return "dictionary"
        case _:
            # this is the default case, when all others are False
            return "other"
