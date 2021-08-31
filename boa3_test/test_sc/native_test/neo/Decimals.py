from boa3.builtin import public
from boa3.builtin.nativecontract.neo import NEO


@public
def main() -> int:
    return NEO.decimals()
