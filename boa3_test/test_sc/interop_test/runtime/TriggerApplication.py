from boa3.sc.compiletime import public
from boa3.sc.runtime import get_trigger
from boa3.sc.types import TriggerType


@public
def Main() -> bool:
    return get_trigger() == TriggerType.APPLICATION
