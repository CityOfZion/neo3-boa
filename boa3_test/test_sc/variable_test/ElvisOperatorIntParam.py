from boa3.sc.compiletime import public


@public
def main(param: int) -> int:
    other = param or 123456
    return other
