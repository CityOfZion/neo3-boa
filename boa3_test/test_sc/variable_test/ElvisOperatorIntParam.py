from boa3.builtin.compile_time import public


@public
def main(param: int) -> int:
    other = param or 123456
    return other
