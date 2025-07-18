from boa3.sc.compiletime import public
from boa3.sc.types import TriggerType


@public
def main(x: TriggerType) -> TriggerType:
    return ~x
