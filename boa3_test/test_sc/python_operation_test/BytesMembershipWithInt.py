from boa3.builtin import public


@public
def main(value: int, some_bytes: bytes) -> bool:
    return value in some_bytes
