from boa3.builtin.compile_time import public


@public
def main(value: int) -> int:
    a = int(value)
    return a
