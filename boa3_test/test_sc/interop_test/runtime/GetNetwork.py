from boa3.sc.compiletime import public
from boa3.sc.runtime import get_network


@public
def main() -> int:
    return get_network()
