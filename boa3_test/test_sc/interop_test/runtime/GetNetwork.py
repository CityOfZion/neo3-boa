from boa3.builtin import public
from boa3.builtin.interop.runtime import get_network


@public
def main() -> int:
    return get_network()
