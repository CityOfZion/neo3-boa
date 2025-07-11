from typing import Any

from boa3.sc.compiletime import public


@public
def main(x: Any) -> str:
    string = "String is: "
    match x:
        case True:
            string += "True"
        case 10:
            string += "10"
        case "2":
            string += "2 string"
        case _:
            # this is the default case, when all others are False
            string += "other"

    return string
