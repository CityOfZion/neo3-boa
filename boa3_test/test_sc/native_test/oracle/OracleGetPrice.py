from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.oracle import Oracle


@public
def main() -> int:
    return Oracle.get_price()
