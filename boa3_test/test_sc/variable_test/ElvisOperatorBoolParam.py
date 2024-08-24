from boa3.sc.compiletime import public


@public
def main(param: bool) -> bool:
    other = param or True
    return other
