from boa3.sc.contracts import NeoToken


def main() -> int:
    return NeoToken.decimals('arg')
