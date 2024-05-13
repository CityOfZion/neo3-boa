from boa3.sc.compiletime import public


@public
def main(b_value: bytes) -> bytes:
    return b_value.lower()
