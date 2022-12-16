from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.neo import NEO


@public
def main() -> str:
    return NEO.symbol()
