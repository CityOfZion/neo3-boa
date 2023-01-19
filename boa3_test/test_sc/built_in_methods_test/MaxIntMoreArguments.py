from boa3.builtin.compile_time import public


@public
def main() -> int:
    return max(4, 1, 16, 8, 2)
