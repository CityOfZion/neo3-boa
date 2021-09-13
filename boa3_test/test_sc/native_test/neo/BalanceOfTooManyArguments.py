from boa3.builtin.nativecontract.neo import NEO
from boa3.builtin.type import UInt160


def main(account: UInt160) -> int:
    return NEO.balanceOf(account, 'arg')
