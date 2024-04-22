from boa3.builtin.compile_time import public


@public
def main(a: list[bool], value: bool) -> int:
    return a.index(value)
