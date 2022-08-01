from boa3.builtin import public


@public
def main(a: bytes, value: bytes) -> int:
    return a.index(value)
