from boa3.builtin.compile_time import public


@public
def main(string: str, substr: str) -> bool:
    return string.startswith(substr)
