from boa3.builtin import public


@public
def main(a: str) -> bytearray:
    b: bytearray = bytearray(a)

    return b
