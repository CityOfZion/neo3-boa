from boa3.sc.compiletime import public
from boa3.sc.types import WitnessScope


@public
def main(x: WitnessScope) -> int:
    return ~x
