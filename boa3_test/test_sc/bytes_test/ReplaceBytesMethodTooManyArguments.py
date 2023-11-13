from boa3.builtin.compile_time import public


@public
def main(string: bytes, old: bytes, new: bytes, count: int) -> bytes:
    return string.replace(old, new, count, count)
