from boa3.builtin.compile_time import public


@public
def main(param: bool) -> bool:
    other = param or True
    return other
