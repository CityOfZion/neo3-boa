from boa3.sc.compiletime import public


@public
def main(x: str) -> str:
    match x:
        case 'first':
            return "1"
        case 'second':
            return "2"
        case "third":
            return "3"
        case _:
            # this is the default case, when all others are False
            return "other"
