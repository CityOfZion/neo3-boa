from boa3.interop.runtime import trigger, TriggerType


def Main() -> bool:
    return trigger() != TriggerType.SYSTEM
