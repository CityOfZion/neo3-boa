from boa3.builtin import public
from boa3.builtin.nativecontract.neo import NEO
from boa3.builtin.type import UInt160


@public
def main(account: UInt160, index: int) -> int:
    return NEO.unclaimed_gas(account, index)
