from boa3.builtin import public


@public
def main(bytes_value: bytes, subbytes_value: bytes, start: int, end: int) -> bool:
    return bytes_value.startswith(subbytes_value, start, end)
