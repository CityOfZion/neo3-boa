from boa3.builtin.compile_time import public


@public
def main(value: int) -> str:
    a = str(value)
    return a
