from boa3.builtin.compile_time import public


@public
def main(value: bytes, some_tuple: tuple[str]) -> bool:
    return value in some_tuple
