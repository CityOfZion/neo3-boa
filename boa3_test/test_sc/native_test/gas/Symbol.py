from boa3.builtin import public
from boa3.builtin.nativecontract.gas import GAS


@public
def main() -> str:
    return GAS.symbol()
