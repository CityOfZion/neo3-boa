from boa3.builtin.compile_time import public


@public
def main(string: str, sep: str) -> list[str]:
    return string.split(sep)
