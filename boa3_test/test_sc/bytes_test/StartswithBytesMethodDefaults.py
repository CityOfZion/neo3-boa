from boa3.builtin.compile_time import public


@public
def main(bytes_value: bytes, subbytes_value: bytes) -> bool:
    return bytes_value.startswith(subbytes_value)
