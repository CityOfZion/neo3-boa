from boa3.builtin.compile_time import public


@public
def main(a: tuple) -> reversed:
    return reversed(a)
