from boa3.builtin import interop, public


@public
def main(test: str) -> bytes:
    return interop.crypto.hash160(test)
