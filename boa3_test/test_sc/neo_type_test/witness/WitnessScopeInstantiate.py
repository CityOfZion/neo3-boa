from boa3.sc.compiletime import public
from boa3.sc.types import WitnessScope


@public
def main(x: int) -> WitnessScope:
    return WitnessScope(x)
