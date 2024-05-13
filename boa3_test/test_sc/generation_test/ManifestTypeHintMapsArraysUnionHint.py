from boa3.sc.compiletime import public


@public
def Main(var: dict[str, list[bool]]) -> list[dict[str, int] | str | bool]:
    if var:
        return []
    return []
