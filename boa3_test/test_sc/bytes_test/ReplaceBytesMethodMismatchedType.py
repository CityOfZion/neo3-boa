from boa3.sc.compiletime import public


@public
def main(string: bytes, old: bytes, new: bytes, count: int) -> bytes:
    return string.replace(count, old, new)
