from boa3.builtin.compile_time import public


@public
def main(value: str, base: int) -> int:
    a = int(value, base)
    return a
