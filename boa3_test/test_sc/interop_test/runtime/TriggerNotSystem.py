from boa3.sc.runtime import get_trigger
from boa3.sc.types import TriggerType


def Main() -> bool:
    return get_trigger() != TriggerType.SYSTEM
