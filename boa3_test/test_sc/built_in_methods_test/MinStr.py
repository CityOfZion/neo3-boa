from boa3.builtin.compile_time import public


@public
def main(val1: str, val2: str) -> str:
    return min(val1, val2)
