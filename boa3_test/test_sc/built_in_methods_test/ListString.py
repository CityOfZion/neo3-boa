from boa3.builtin.compile_time import public


@public
def main(x: str) -> list[str]:
    return list(x)
