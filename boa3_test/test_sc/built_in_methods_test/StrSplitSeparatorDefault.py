from boa3.builtin.compile_time import public


@public
def main(string: str) -> list[str]:
    return string.split()
