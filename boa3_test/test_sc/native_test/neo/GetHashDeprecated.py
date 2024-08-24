from boa3.builtin.nativecontract.neo import NEO
from boa3.sc.compiletime import public
from boa3.sc.types import UInt160


@public
def main() -> UInt160:
    return NEO.hash
