from boa3.builtin import public


@public
def main(value: str, some_bytes: bytes) -> bool:
    return value not in some_bytes
