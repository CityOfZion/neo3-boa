from boa3.builtin.compile_time import public


@public
def main() -> int:
    a = []
    return a.count(1)
