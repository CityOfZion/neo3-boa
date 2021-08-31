from boa3.builtin.nativecontract.neo import NEO


def main() -> int:
    return NEO.decimals('arg')
