from boa3.builtin import public


@public
def main(a: str, value: str) -> int:
    return a.index(value)
