from boa3.builtin.compile_time import public


@public
def main(string: str, chars: str) -> str:
    return string.strip(chars)
