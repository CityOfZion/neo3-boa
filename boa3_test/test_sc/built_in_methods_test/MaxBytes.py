from boa3.builtin import public


@public
def main(val1: bytes, val2: bytes) -> bytes:
    return max(val1, val2)
