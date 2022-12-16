from boa3.builtin.compile_time import public


@public
def main(value: bool) -> str:
    a = str(value)
    return a
