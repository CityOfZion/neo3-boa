from boa3.builtin.compile_time import public


@public
def main(x: bool) -> str:
    match x:
        case True:
            return "True"
        case False:
            return "False"

    return "bool not provided"
