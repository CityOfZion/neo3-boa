from boa3.sc.compiletime import public
from boa3.sc.contracts import GasToken


@public
def main() -> int:
    return GasToken.totalSupply()
