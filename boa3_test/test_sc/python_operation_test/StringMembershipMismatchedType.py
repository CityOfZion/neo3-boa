from boa3.builtin.compile_time import public


@public
def main(value: bytes, some_string: str) -> bool:
    return value not in some_string
