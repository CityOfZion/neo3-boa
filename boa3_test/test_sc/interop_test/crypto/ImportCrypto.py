from boa3.sc.compiletime import public
from boa3.builtin.interop import crypto


@public
def main(test: str) -> bytes:
    return crypto.hash160(test)
