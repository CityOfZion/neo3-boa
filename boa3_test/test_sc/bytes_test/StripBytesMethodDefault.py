from boa3.builtin import public


@public
def main(bytes_value: bytes) -> bytes:
    return bytes_value.strip()
