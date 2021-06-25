from boa3.builtin import public
from boa3.builtin.interop import Oracle


@public
def main() -> int:
    return Oracle.get_price()
