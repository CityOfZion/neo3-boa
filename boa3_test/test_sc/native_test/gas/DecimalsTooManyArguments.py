from boa3.sc.contracts import GasToken


def main() -> int:
    return GasToken.decimals('arg')
