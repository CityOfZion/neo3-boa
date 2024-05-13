from boa3.sc.compiletime import public
from boa3.builtin.nativecontract.oracle import Oracle
from boa3.sc.types import UInt160


@public
def main() -> UInt160:
    return Oracle.hash
