from boa3.builtin.compile_time import public


@public
def main(a: str, b: str) -> int:
    if a > b:
        return 3
    return 2
