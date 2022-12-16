from boa3.builtin.compile_time import public


@public
def main(value: int, some_bytes: bytes) -> bool:
    return value in some_bytes
