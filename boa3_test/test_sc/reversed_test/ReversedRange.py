from boa3.builtin.compile_time import public


@public
def main() -> reversed:
    return reversed(range(3))
