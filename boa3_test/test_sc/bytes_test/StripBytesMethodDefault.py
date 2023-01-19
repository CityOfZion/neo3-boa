from boa3.builtin.compile_time import public


@public
def main(bytes_value: bytes) -> bytes:
    return bytes_value.strip()
