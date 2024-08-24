from boa3.sc.compiletime import public


@public
def main(x: bytes) -> bool:
    return bool(x)
