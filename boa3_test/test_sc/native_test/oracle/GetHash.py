from boa3.builtin import public
from boa3.builtin.nativecontract.oracle import Oracle
from boa3.builtin.type import UInt160


@public
def main() -> UInt160:
    return Oracle.hash
