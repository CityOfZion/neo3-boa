from boa3.builtin.compile_time import public


@public
def main(val1: bytes, val2: bytes) -> bytes:
    return min(val1, val2)
