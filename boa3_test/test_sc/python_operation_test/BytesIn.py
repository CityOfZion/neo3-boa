from boa3.builtin import public


@public
def main(value: bytes, some_bytes: bytes) -> bool:
    return value in some_bytes
