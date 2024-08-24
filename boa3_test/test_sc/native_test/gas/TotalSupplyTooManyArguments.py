from boa3.sc.contracts import GasToken


def main() -> int:
    return GasToken.totalSupply('arg')
