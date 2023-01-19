from boa3.builtin.compile_time import public


@public
def main() -> int:
    return min(2, 8, 1, 4, 16)
