from boa3.builtin import public


@public
def main(a: str, b: str) -> int:
    if a > b:
        return 3
    return 2
