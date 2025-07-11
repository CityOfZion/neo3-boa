from boa3.sc.compiletime import public
from boa3.sc.types import WitnessRuleAction


@public
def main(x: int) -> WitnessRuleAction:
    return WitnessRuleAction(x)
