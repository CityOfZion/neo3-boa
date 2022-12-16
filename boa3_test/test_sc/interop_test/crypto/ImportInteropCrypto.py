from boa3.builtin import interop
from boa3.builtin.compile_time import public


@public
def main(test: str) -> bytes:
    return interop.crypto.hash160(test)
