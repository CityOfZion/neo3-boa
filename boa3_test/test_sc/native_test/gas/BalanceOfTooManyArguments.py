from boa3.builtin.nativecontract.gas import GAS
from boa3.builtin.type import UInt160


def main(account: UInt160) -> int:
    return GAS.balanceOf(account, 'arg')
