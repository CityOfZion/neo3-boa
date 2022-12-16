from boa3.builtin.compile_time import public


@public
def main(a: bytes, value: bytes) -> int:
    return a.index(value)
