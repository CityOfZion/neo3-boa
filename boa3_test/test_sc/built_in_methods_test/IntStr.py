from boa3.builtin import public


@public
def main(value: str, base: int) -> int:
    a = int(value, base)
    return a
