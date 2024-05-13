from boa3.sc.contracts import NeoToken


def main() -> str:
    return NeoToken.symbol('arg')
