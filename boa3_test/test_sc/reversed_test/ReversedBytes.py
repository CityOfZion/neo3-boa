from boa3.builtin import public


@public
def main(a: bytes) -> reversed:
    return reversed(a)
