from boa3.builtin import public
from boa3.builtin.interop.oracle import Oracle


@public
def main() -> int:
    return Oracle.get_price()
