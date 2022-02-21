from boa3.builtin import public


@public
def main(value: bytes, base: int) -> int:
    a = int(value, base)
    return a
