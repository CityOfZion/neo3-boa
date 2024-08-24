from boa3.builtin.interop import crypto
from boa3.sc.compiletime import public


@public
def main(test: str) -> bytes:
    return crypto.hash160(test)
