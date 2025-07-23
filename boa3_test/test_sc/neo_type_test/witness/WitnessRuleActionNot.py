from boa3.sc.compiletime import public
from boa3.sc.types import WitnessRuleAction


@public
def main(x: WitnessRuleAction) -> int:
    return ~x
