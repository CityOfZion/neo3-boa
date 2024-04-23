from boa3.builtin.compile_time import public


@public
def main(a: list[str], b: str) -> bool:
    return a[0] == b
