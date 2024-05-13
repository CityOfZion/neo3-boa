from boa3.sc.compiletime import public


@public
def main(param: str | None) -> str | None:
    other = param or "some default value"
    return other
