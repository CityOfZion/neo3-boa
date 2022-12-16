from boa3.builtin.compile_time import public


@public
def main(value: bytes, base: int) -> int:
    a = int(value, base)
    return a
