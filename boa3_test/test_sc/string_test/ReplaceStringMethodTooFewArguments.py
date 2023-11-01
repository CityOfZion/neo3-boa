from boa3.builtin.compile_time import public


@public
def main(string: str, old: str, new: str, count: int) -> str:
    return string.replace(old)
