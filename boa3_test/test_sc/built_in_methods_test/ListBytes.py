from boa3.sc.compiletime import public


@public
def main(x: bytes) -> list[int]:
    return list(x)


def verify_return() -> list[int]:
    return list(b'123')
