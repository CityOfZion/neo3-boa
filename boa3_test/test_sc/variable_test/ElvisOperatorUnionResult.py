from boa3.sc.compiletime import public


@public
def main(param: int) -> str | int:
    other = param or "some default value"
    return other
