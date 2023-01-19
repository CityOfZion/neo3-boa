from boa3.builtin.compile_time import public


@public
def main(b_value: bytes) -> bytes:
    return b_value.upper()
