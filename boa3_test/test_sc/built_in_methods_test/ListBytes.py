from boa3.builtin.compile_time import public


@public
def main(x: bytes) -> list[int]:
    return list(x)


def verify_return() -> list[int]:
    return list(b'123')
