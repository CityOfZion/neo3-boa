from boa3.builtin.compile_time import public


@public
def main() -> int:
    a = 1
    b = 2
    c = a + b
    return c
