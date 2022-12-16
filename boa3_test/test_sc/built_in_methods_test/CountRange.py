from boa3.builtin.compile_time import public


@public
def main() -> int:
    return range(10).count(1)
