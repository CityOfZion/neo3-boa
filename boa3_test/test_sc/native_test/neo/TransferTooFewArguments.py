from boa3.builtin.nativecontract.neo import NEO
from boa3.builtin.type import UInt160


def main(from_address: UInt160, to_address: UInt160) -> int:
    return NEO.transfer(from_address, to_address)
