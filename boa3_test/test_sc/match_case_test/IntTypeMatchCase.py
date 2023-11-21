from boa3.builtin.compile_time import public


@public
def main(x: int) -> str:
    match x:
        case 10:
            return "ten"
        case -10:
            return "minus ten"
        case 0:
            return "zero"
        case _:
            # this is the default case, when all others are False
            return "other"
