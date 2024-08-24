from boa3.sc.compiletime import public
from boa3.sc.contracts import GasToken


@public
def main() -> str:
    return GasToken.symbol()
