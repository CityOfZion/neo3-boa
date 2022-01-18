from boa3.builtin import public


@public
def main(x: bytes) -> bool:
    return bool(x)
