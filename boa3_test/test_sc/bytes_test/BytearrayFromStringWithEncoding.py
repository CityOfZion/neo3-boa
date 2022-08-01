from boa3.builtin import public


@public
def main(a: str) -> bytearray:
    b: bytearray = bytearray(a, 'utf-8')

    return b
