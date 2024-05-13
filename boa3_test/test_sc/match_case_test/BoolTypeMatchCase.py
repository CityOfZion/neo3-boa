from boa3.sc.compiletime import public


@public
def main(x: bool) -> str:
    match x:
        case True:
            return "True"
        case False:
            return "False"

    return "bool not provided"
