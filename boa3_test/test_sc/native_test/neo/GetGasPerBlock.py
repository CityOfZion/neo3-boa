from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.neo import NEO


@public
def main() -> int:
    return NEO.get_gas_per_block()
