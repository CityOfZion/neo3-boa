from boa3.sc.compiletime import public


@public
def main(bytes_value: bytes) -> str:
    return bytes_value.hex()


@public
def bytes_dot_hex(bytes_value: bytes) -> str:
    return bytes.hex(bytes_value)


@public
def literal_bytes() -> str:
    return b'0123456789abcdef'.hex()
