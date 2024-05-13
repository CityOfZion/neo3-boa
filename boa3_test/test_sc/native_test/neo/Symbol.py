from boa3.sc.compiletime import public
from boa3.sc.contracts import NeoToken


@public
def main() -> str:
    return NeoToken.symbol()
