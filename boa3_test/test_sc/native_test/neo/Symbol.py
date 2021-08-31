from boa3.builtin import public
from boa3.builtin.nativecontract.neo import NEO


@public
def main() -> str:
    return NEO.symbol()
