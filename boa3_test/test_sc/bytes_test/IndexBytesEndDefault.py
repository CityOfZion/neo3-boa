from boa3.builtin.compile_time import public


@public
def main(a: bytes, value: bytes, start: int) -> int:
    return a.index(value, start)
