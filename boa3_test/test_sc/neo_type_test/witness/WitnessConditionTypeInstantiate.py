from boa3.sc.compiletime import public
from boa3.sc.types import WitnessConditionType


@public
def main(x: int) -> WitnessConditionType:
    return WitnessConditionType(x)
