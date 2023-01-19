from boa3.builtin.compile_time import public


@public
def main(a: bytes) -> reversed:
    return reversed(a)
