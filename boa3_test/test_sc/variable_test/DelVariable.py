from boa3.builtin.compile_time import public


@public
def main() -> int:
    a = 123
    del a

    return 123
