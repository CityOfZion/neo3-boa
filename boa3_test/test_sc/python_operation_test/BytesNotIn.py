from boa3.builtin.compile_time import public


@public
def main(value: bytes, some_bytes: bytes) -> bool:
    return value not in some_bytes
