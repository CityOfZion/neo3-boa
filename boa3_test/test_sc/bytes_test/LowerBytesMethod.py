from boa3.builtin import public


@public
def main(b_value: bytes) -> bytes:
    return b_value.lower()
