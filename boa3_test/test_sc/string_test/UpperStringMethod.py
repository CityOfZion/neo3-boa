from boa3.builtin.compile_time import public


@public
def main(string: str) -> str:
    return string.upper()
