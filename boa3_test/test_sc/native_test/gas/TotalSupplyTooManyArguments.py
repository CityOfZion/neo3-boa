from boa3.builtin.nativecontract.gas import GAS


def main() -> int:
    return GAS.totalSupply('arg')
