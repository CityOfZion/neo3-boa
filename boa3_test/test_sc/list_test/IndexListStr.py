from boa3.builtin.compile_time import public


@public
def main(a: list[str], value: str) -> int:
    return a.index(value)
