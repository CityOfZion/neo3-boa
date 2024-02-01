from boa3.builtin.compile_time import public


@public
def main(param: str) -> str:
    other = param or "some default value"
    return other
